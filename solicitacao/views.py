import logging
import os
from fileinput import filename
from pprint import pprint
import tempfile

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.views.generic import DetailView, View
from django.views.generic.list import ListView
from docx import Document
from htmldocx import HtmlToDocx
from solicita.storage_backends import PublicMediaStorage
from xhtml2pdf import pisa

from .models import Solicitacao


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
        pprint(solicitacao.secretaria.prefeitura.logotipo.open())
        pprint(dir(solicitacao.secretaria.prefeitura.logotipo))
        pprint(vars(solicitacao.secretaria.prefeitura.logotipo))
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
        solicitacao = solicitacao.select_related('secretaria')
        context = {'solicitacao': solicitacao}
        template = get_template(template_path)
        html = template.render(context)
        media_storage: PublicMediaStorage = PublicMediaStorage()
        default_doc: PublicMediaStorage = media_storage.open('default.docx')
        document: Document = Document(docx=default_doc)
        docx: HtmlToDocx = HtmlToDocx()
        docx.add_html_to_document(html, document)
        tempdir = tempfile.mkdtemp()
        document.save(os.path.join(tempdir, 'report.docx'))
        with open(os.path.join(tempdir, 'report.docx'), "rb") as doc_ok:
            response: HttpResponse = HttpResponse(doc_ok,
                                                  content_type='application/docx')
            response['Content-Disposition'] = 'attachment; filename="report.docx"'
        return response
