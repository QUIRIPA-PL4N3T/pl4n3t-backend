import ssl
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django_pdfkit import PDFView
from reports.models import ReportTemplate
from companies.models import Company
import functools
from django.conf import settings
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher


class ReportPDFDetailView(PDFView):
    template_name = 'reports/basic-template.html'
    inline = True
    model = ReportTemplate
    object = None
    # pdfkit_options = {
    #     'page-size': 'Letter',
    #     'margin-top': '0.75in',
    #     'margin-right': '0.75in',
    #     'margin-bottom': '0.75in',
    #     'margin-left': '0.75in',
    #     'encoding': "UTF-8",
    #     'custom-header': [
    #         ('Accept-Encoding', 'gzip')
    #     ],
    #     'no-outline': None
    # }

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        report = get_object_or_404(ReportTemplate, id=id_)
        self.object = report
        return report

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context["company"] = Company.objects.first()
        context.update(kwargs)
        return super().get_context_data(**context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ReportPDFDetailView, self).get(request, *args, **kwargs)


class MyDetailView(DetailView):
    # vanilla Django DetailView
    template_name = 'reports/basic2-template.html'


def custom_url_fetcher(url, *args, **kwargs):
    # rewrite requests for CDN URLs to file path in STATIC_ROOT to use local file
    cloud_storage_url = 'https://s3.amazonaws.com/django-weasyprint/static/'
    print('******************')
    print(url)
    print('******************')
    if url.startswith(cloud_storage_url):
        url = 'file://' + url.replace(cloud_storage_url, settings.STATIC_URL)
    new_url = django_url_fetcher(url, *args, **kwargs)
    print('******************')
    print(new_url)
    print('******************')
    return new_url


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to pass a kwarg to URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(custom_url_fetcher, ssl_context=context)


class PrintView(WeasyTemplateResponseMixin, MyDetailView):
    # output of MyDetailView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        settings.STATIC_ROOT + '/css/report.css',
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse

    queryset = ReportTemplate.objects.all()

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context["company"] = Company.objects.first()
            context["report"] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)


class DownloadView(WeasyTemplateResponseMixin, MyDetailView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'foo.pdf'


class DynamicNameView(WeasyTemplateResponseMixin, MyDetailView):
    # dynamically generate filename
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )
