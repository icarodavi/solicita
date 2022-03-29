import os
from io import BytesIO
from xhtml2pdf import pisa
import boto3

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
        solicitacao = Solicitacao.objects.filter(pk=kwargs.get('pk')).first()
        context = {'solicitacao': solicitacao}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

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
        solicitacao = Solicitacao.objects.filter(pk=kwargs.get('pk')).first()
        context = {'solicitacao': solicitacao}
        media_storage = PublicMediaStorage()
        # s3: boto3 = boto3.resource('s3',
        #                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #                            aws_secret_key=settings.AWS_SECRET_ACCESS_KEY
        #                            )
        # boto = s3.Bucket('solicitacao')
        # Cria um objeto do tipo RESPONSE DJANGO e especifica o content_type como pdf
        # Busca o template e o renderiza
        template = get_template(template_path)
        html = template.render(context)
        # Cria o arquivo DOCX
        # docx_path = storage.open(
        #     str(settings.MEDIA_ROOT) + str('report.docx'), "r")
        # print(docx_path)
        default_doc: PublicMediaStorage = media_storage.open('default.docx')
        document: Document = Document(docx=default_doc)
        default_doc.close()
        docx: HtmlToDocx = HtmlToDocx()
        docx.closed = False
        docx.add_html_to_document(html, document)
        document.save('report.docx')
        print(document.__dict__)
        media_storage.save('report.docx', document)
        # with open('report.docx', "rb") as doc_ok:
        # with open(ContentFile(doc_buffer.getvalue()), "rb") as doc:
        response = HttpResponse(media_storage.location,
                                content_type='application/docx')
        response['Content-Disposition'] = 'attachment; filename="report.docx"'
        # return DownloadResponse(self.request, str(settings.MEDIA_ROOT), 'report.docx')
        # docx_path.close()
        return response
