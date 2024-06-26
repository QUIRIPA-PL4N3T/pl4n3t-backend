from django import forms
from django.contrib import admin
from reports.models import Report, ReportTemplate, CompanyTemplate
from django.utils.translation import gettext_lazy as _


class ReportTemplateAdminForm(forms.ModelForm):
    EXCLUDE_FIELDS = ['id', 'name', 'version', 'period', 'creation_date', 'fields_ordered', 'report']

    class Meta:
        model = ReportTemplate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model_fields = ReportTemplate._meta.get_fields()
        field_choices = [
            (field.name, self.instance.get_field_display_name(field.name))
            for field in model_fields
            if field.name not in self.EXCLUDE_FIELDS]

        self.fields['fields_ordered'] = forms.MultipleChoiceField(
            label=_('Secciones del Reporte'),
            choices=field_choices,
            widget=forms.SelectMultiple(attrs={'size': '10'}),
            required=False,
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_fields = self.cleaned_data['fields_ordered']
        instance.fields_ordered = ','.join(selected_fields)
        if commit:
            instance.save()
        return instance


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    form = ReportTemplateAdminForm
    list_display = ['id', 'name', 'version']
    list_filter = ['tags']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj): # noqa
        return u", ".join(o.name for o in obj.tags.all())

    fieldsets = (
        (_('General Information'), {
            'fields': ('name', 'version', 'tags', 'fields_ordered')
        }),
        (_('Contenido'), {
            'fields':
                ('introduction',
                 'definitions',
                 'company_description',
                 'organizational_description',
                 'baseline_year_diagnostic',
                 'report_frequency',
                 'intended_use',
                 'diagnostic_scope',
                 'diagnostic_objectives',
                 'quantification_methodology',
                 'emissions_inventory_exclusions',
                 'carbon_footprint_determination',
                 'gei_inventory_boundaries',
                 'report_results',
                 'emissions_inventory',
                 'emissions_consolidation',
                 'emissions_consolidation_year',
                 'carbon_footprint_quantification',
                 'emissions_reduction_recommendations',
                 'conclusions',
                 'annexes'),
            'classes': ('collapse',)  # This will make the PDF Report section collapsible
        }),
    )


@admin.register(CompanyTemplate)
class CompanyTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'company', 'version']
    list_filter = ['company', 'tags']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'company', 'version', 'period', 'is_finalized', 'tags')
        }),
        ('PDF Report', {
            'fields': ('pdf_report',),
            'classes': ('collapse',)  # This will make the PDF Report section collapsible
        }),
        ('Report Sections', {
            'fields': (
                'introduction', 'definitions', 'company_description', 'organizational_description',
                'baseline_year_diagnostic', 'report_frequency', 'intended_use', 'diagnostic_scope',
                'diagnostic_objectives', 'quantification_methodology', 'emissions_inventory_exclusions',
                'carbon_footprint_determination', 'gei_inventory_boundaries', 'report_results',
                'emissions_inventory', 'emissions_consolidation', 'emissions_consolidation_year',
                'carbon_footprint_quantification', 'emissions_reduction_recommendations', 'conclusions',
                'annexes'
            ),
            'classes': ('collapse',)  # This will make the Report Sections collapsible
        }),
        ('Fields Order', {
            'fields': ('fields_ordered',),
        }),
    )

    list_display = ('id', 'name', 'company', 'version', 'period', 'is_finalized')
    list_filter = ['company', 'tags', 'is_finalized']
    search_fields = ['name', 'company__name', 'period']
    ordering = ['company', 'name', 'version']
    filter_horizontal = ('tags',)

    def get_queryset(self, request):
        """Limit each user to see only their own reports unless they are a superuser."""
        qs = super(ReportAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company__user=request.user)

    def save_model(self, request, obj, form, change):
        """Set the user to the current user when creating a new report."""
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
