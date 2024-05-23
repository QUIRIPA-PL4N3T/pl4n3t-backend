from ckeditor.fields import RichTextField
from django.core.files.base import ContentFile
from django.db import models
from django.http import HttpResponse
from django.template.loader import get_template
from taggit.managers import TaggableManager
from xhtml2pdf import pisa
from django.utils.translation import gettext_lazy as _


class Template(models.Model):
    # General report information
    name = models.CharField(_('Nombre'), max_length=200)
    creation_date = models.DateField(auto_now_add=True, null=True, blank=True)
    version = models.FloatField(_('Versión'), default=1.0, blank=True)

    # Report sections
    introduction = RichTextField(
        _('Introducción'), blank=True)
    definitions = RichTextField(
        _('Definiciones'), blank=True)
    company_description = RichTextField(
        _('Descripción de la Empresa'), blank=True)
    organizational_description = RichTextField(
        _('Descripción Organizacional que realiza el diagnostico'), blank=True)
    baseline_year_diagnostic = RichTextField(
        _('Año base diagnostico e informe'), blank=True)
    report_frequency = RichTextField(
        _('Frecuencia del Informe'), blank=True)
    intended_use = RichTextField(
        _('Uso previsto y usuarios y usuarios previstos del informe'), blank=True)
    diagnostic_scope = RichTextField(
        _('Alcance del diagnostico'), blank=True)
    diagnostic_objectives = RichTextField(
        _('Objetivos del Diagnostico e Informe'), blank=True)
    quantification_methodology = RichTextField(
        _('Metodología de Cuantificación'), blank=True)
    emissions_inventory_exclusions = RichTextField(
        _('Exclusiones del inventario de las fuentes de Emisión'), blank=True)
    carbon_footprint_determination = RichTextField(
        _('Determinación de la Huella de Carbono'), blank=True)
    gei_inventory_boundaries = RichTextField(
        _('Limites del inventario de GEI'), blank=True)
    report_results = RichTextField(
        _('Resultados del informe'), blank=True)
    emissions_inventory = RichTextField(
        _('Inventario de Cuantificación de emisiones gei organizacionales'), blank=True)
    emissions_consolidation = RichTextField(
        _('Consolidado del inventario de emisiones de gei generadas Año/periodo'), blank=True)
    emissions_consolidation_year = RichTextField(
        _('Consolidado gei emitidas durante el año'), blank=True)
    carbon_footprint_quantification = RichTextField(
        _('Cuantificación huella de carbono'), blank=True)
    emissions_reduction_recommendations = RichTextField(
        _('Recomendaciones en reducciones de emisiones de GEI'), blank=True)
    conclusions = RichTextField(
        _('Conclusiones'), blank=True)
    annexes = RichTextField(
        _('Anexos'), blank=True)

    # Report Fields order
    fields_ordered = models.CharField(
        _('Secciones del Reporte'), max_length=1024, blank=True)

    class Meta:
        abstract = True


class ReportTemplate(Template):
    tags = TaggableManager()

    def content_list(self) -> list:
        return self.fields_ordered.split(',')

    def get_field_display_name(self, field_name):
        try:
            field = self._meta.get_field(field_name)
            return field.verbose_name
        except AttributeError:
            return field_name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Plantilla de Pl4n3t')
        verbose_name_plural = _('Plantillas de Pl4n3t')


class CompanyTemplate(Template):
    tags = TaggableManager(blank=True)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} - Version {self.version}"

    class Meta:
        verbose_name = _('Plantilla de Compañía')
        verbose_name_plural = _('Plantillas de Compañía')


class Report(Template):
    tags = TaggableManager(blank=True)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    period = models.CharField(max_length=10)

    # Additional fields for PDF report storage
    pdf_report = models.FileField(upload_to='generated_reports/', blank=True, null=True)

    # A flag to indicate if the report is finalized and cannot be modified
    is_finalized = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check if the report is finalized, then set is_finalized to True
        if self.is_finalized:
            self.pdf_report.read_only = True
        super(Report, self).save(*args, **kwargs)

    def generate_pdf_report(self):
        # Generate the PDF report from HTML content
        template = get_template('reports/report_template.html')
        context = {'report_content': self.template.content}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=sustainability_report_{self.id}.pdf'
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        else:
            self.pdf_report.save(response['Content-Disposition'], ContentFile(response.content))

    def __str__(self):
        return f"{self.name} - Version {self.version} - Period {self.period}"

    class Meta:
        verbose_name = _('Reporte')
        verbose_name_plural = _('Reportes')
