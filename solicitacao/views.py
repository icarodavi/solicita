import os
import tempfile
from pprint import pprint

from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  UpdateView, View)
from django.views.generic.list import ListView
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from htmldocx import HtmlToDocx
from solicita.storage_backends import PublicMediaStorage
from xhtml2pdf import pisa

from .models import Solicitacao
from .forms import SolicitacaoForm


class SolicitacaoIndex(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = 'solicitacao/index.html'
    context_object_name = 'solicitacoes'
    paginate_by = 10

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.select_related('secretaria')
        return query_set


class SolicitacaoDetailView(LoginRequiredMixin, DetailView):
    model = Solicitacao
    template_name = "solicitacao/solicitacao.html"
    context_object_name = 'solicitacao'

    # def get(self):
    #     return render(self.request, self.template_name)
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.select_related()


class SolicitacaoPDF(LoginRequiredMixin, View):
    model = Solicitacao
    template_name = 'solicitacao/render_pdf.html'
    context_object_name = 'solicitacao'

    def get(self, *args, **kwargs):
        template_path = self.template_name
        solicitacao = Solicitacao.objects.filter(pk=kwargs.get('pk'))
        solicitacao = solicitacao.select_related('secretaria').first()
        context = {'solicitacao': solicitacao}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # pprint(solicitacao.secretaria.prefeitura.logotipo.open())
        # pprint(dir(solicitacao.secretaria.prefeitura.logotipo))
        # pprint(vars(solicitacao.secretaria.prefeitura.logotipo))
        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class SolicitacaoDOCX(LoginRequiredMixin, View):
    model = Solicitacao
    template_name = 'solicitacao/render_doc.html'
    context_object_name = 'solicitacao'

    def get(self, *args, **kwargs):
        template_path = self.template_name
        solicitacao = Solicitacao.objects.filter(pk=kwargs.get('pk'))
        solicitacao = solicitacao.select_related('secretaria').first()
        context = {'solicitacao': solicitacao}
        template = get_template(template_path)
        html = template.render(context)
        media_storage: PublicMediaStorage = PublicMediaStorage()
        default_doc: PublicMediaStorage = media_storage.open('default.docx')
        document: Document = Document(docx=default_doc)
        docx: HtmlToDocx = HtmlToDocx()
        docx.add_html_to_document(html, document)
        # pprint(dir(solicitacao.first().secretaria.prefeitura.get_logo))
        # pprint(vars(solicitacao.first().secretaria.prefeitura.get_logo))
        section = document.sections[0]
        header = section.header
        # paragraph = header.paragraphs[0]
        # paragraph.add_picture(
        #     solicitacao.first().secretaria.prefeitura.get_logo)
        # paragraph.text = '\t{}'.format(solicitacao.secretaria.prefeitura)
        # document.add_picture(solicitacao.secretaria.prefeitura.get_logo())
        header_table = header.add_table(1, 2, Inches(6))
        header_table_cells = header_table.rows[0].cells
        header_table_0 = header_table_cells[0].add_paragraph()
        kh = header_table_0.add_run()
        kh.add_picture(
            solicitacao.secretaria.prefeitura.get_logo(), width=Inches(1))
        header_table_1 = header_table_cells[1].add_paragraph(
            solicitacao.secretaria.prefeitura.get_prefeitura()+'\n'+solicitacao.secretaria.nome+'\n'+solicitacao.secretaria.endereco)
        header_table_1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        # p2 = header.paragraphs[1]
        # p2.text = solicitacao.secretaria.nome
        tempdir = tempfile.mkdtemp()
        document.save(os.path.join(tempdir, 'report.docx'))
        with open(os.path.join(tempdir, 'report.docx'), "rb") as doc_ok:
            response: HttpResponse = HttpResponse(doc_ok,
                                                  content_type='application/docx')
            response['Content-Disposition'] = 'attachment; filename="report.docx"'
        return response


class SolicitacaoCreateView(LoginRequiredMixin, View):
    model = Solicitacao
    template_name = 'solicitacao/form.html'
    fields = '__all__'
    success_url = 'solicitacao:index'

    def get(self, *args, **kwargs):
        form = SolicitacaoForm()
        return render(self.request, 'solicitacao/form.html', {'form': form})

    def post(self, *args, **kwargs):
        form = SolicitacaoForm(data=self.request.POST,
                               files=self.request.FILES)
        if form.is_valid():
            form.save()
            return redirect('solicitacao:index')
        else:
            return render(self.request, 'solicitacao/form.html', {'form': form})


class SolicitacaoEdit(LoginRequiredMixin, UpdateView):
    model = Solicitacao
    template_name = 'solicitacao/edit.html'
    # fields = '__all__'
    form_class = SolicitacaoForm
    success_url = reverse_lazy('solicitacao:index')


class SolicitacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Solicitacao
    template_name = "produto/delete.html"
    success_url = reverse_lazy('produto:index')
