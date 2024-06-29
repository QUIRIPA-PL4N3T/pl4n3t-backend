from datetime import datetime
from django.conf import settings
from django.db.models import Sum, F, Prefetch
from django.utils import timezone
from activities.models import ActivityGasEmitted, ActivityGasEmittedByFactor, Activity
from companies.models import Company


class DataAnalysis(object):
    company = None
    company_id = None
    location_id = None
    category_id = None
    scope_id = None
    group_id = None
    source_type_id = None
    factor_type_id = None
    initial_date = None
    end_date = None
    year = None
    month = None
    filters = {}
    gases_emitted_by_factor = ActivityGasEmittedByFactor.objects.none()
    filtered_activities = Activity.objects.none()

    results = {}

    def __init__(self, company_id, location_id=None, scope_id=None, group_id=None, source_type_id=None, factor_id=None,
                 category_id=None, factor_type_id=None, initial_date=None, end_date=None, year=None, month=None,
                 emission_source_id=None):

        if not company_id:
            raise ValueError("company_id is required")

        self.company_id = company_id
        try:
            self.company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise ValueError("Company does not exist")

        self.location_id = location_id
        self.scope_id = scope_id
        self.category_id = category_id
        self.group_id = group_id
        self.emission_source_id = emission_source_id
        self.source_type_id = source_type_id
        self.factor_type_id = factor_type_id
        self.factor_id = factor_id
        self.initial_date = initial_date
        self.end_date = end_date
        self.year = year
        self.month = month
        self.data = {}

    def emissions_by_gas(self):
        # Collect data for the summary of emissions emitted by gas
        gases_emitted = self.gases_emitted_by_factor.values('greenhouse_gas__name').annotate(
            total_value=Sum('value')
        ).order_by('greenhouse_gas__name')
        gas_summary = []

        for gas in gases_emitted:
            percentage_change = self.calculate_percentage_change(gas['greenhouse_gas__name'])
            gas_summary.append({
                'gas_name': gas['greenhouse_gas__name'],
                'total_value': gas['total_value'],
                'percentage_change': percentage_change
            })

        self.data['gas_emissions'] = gas_summary
        return gas_summary

    def emissions_by_source(self):
        # Collect data for the summary by emission source type
        emission_sources = self.gases_emitted_by_factor.values('activity__emission_source__name').annotate(
            value=Sum('co2e')
        ).order_by('activity__emission_source__name')
        source_summary = [
            {'source_type': source['activity__emission_source__name'], 'value': source['value']} for source in
            emission_sources]

        self.data['emission_sources'] = source_summary
        return source_summary

    def emissions_by_classification_group(self):
        # Collect data for GHG distribution
        gei_distribution = self.gases_emitted_by_factor.values('co2e').annotate(
            percentage=F('co2e') / Sum('co2e') * 100
        )
        gei_summary = [{'category': 'GEI', 'percentage': gei['percentage']} for gei in gei_distribution]

        self.data['gei_distribution'] = gei_summary
        return gei_summary

    def get_total_co2e(self):
        self.data['total_emissions'] = self.gases_emitted_by_factor.aggregate(total=Sum('co2e'))['total']
        return self.data['total_emissions']

    def calculate_percentage_change(self, gas_name):
        current_month = timezone.now().month
        previous_month = current_month - 1 if current_month > 1 else 12

        current_month_emissions = self.gases_emitted_by_factor.filter(
            activity__date__month=current_month,
            greenhouse_gas__name=gas_name
        ).aggregate(total=Sum('value'))['total'] or 0

        previous_month_emissions = self.gases_emitted_by_factor.filter(
            activity__date__month=previous_month,
            greenhouse_gas__name=gas_name
        ).aggregate(total=Sum('value'))['total'] or 0

        if previous_month_emissions == 0:
            return 100

        percentage_change = ((current_month_emissions - previous_month_emissions) / previous_month_emissions) * 100
        return percentage_change

    def emissions_by_source_type_and_scope(self):
        data = self.gases_emitted_by_factor.values(
            'activity__emission_source__source_type__name', 'activity__emission_source__group__category__scope__name'
        ).annotate(
            value=Sum('co2e')
        ).order_by('activity__emission_source__source_type__name', 'activity__emission_source__group__category__scope__name')

        summary = [
            {
                'source_type': item['activity__emission_source__source_type__name'],
                'scope': item['activity__emission_source__group__category__scope__name'],
                'value': item['value']
            }
            for item in data
        ]

        self.data['emissions_by_source_type_and_scope'] = summary
        return summary

    def emissions_by_scope(self):
        data = self.gases_emitted_by_factor.values(
            'activity__emission_source__group__category__scope__name'
        ).annotate(
            value=Sum('co2e')
        ).order_by('activity__emission_source__group__category__scope__name')

        summary = [
            {
                'scope': item['activity__emission_source__group__category__scope__name'],
                'value': item['value']
            }
            for item in data
        ]

        self.data['emissions_by_scope'] = summary
        return summary

    def emissions_direct_and_indirect(self):
        data = self.gases_emitted_by_factor.values(
            'activity__emission_source__source_type__name'
        ).annotate(
            value=Sum('co2e')
        ).order_by('activity__emission_source__source_type__name')

        summary = [
            {
                'emission_type': item['activity__emission_source__source_type__name'],
                'value': item['value']
            }
            for item in data
        ]

        self.data['emissions_direct_and_indirect'] = summary
        return summary

    def gases_emitted_by_scope(self):
        data = self.gases_emitted_by_factor.values(
            'activity__emission_source__group__category__scope__name', 'greenhouse_gas__name'
        ).annotate(
            value=Sum('value')
        ).order_by('activity__emission_source__group__category__scope__name', 'greenhouse_gas__name')

        summary = [
            {
                'scope': item['activity__emission_source__group__category__scope__name'],
                'gas_name': item['greenhouse_gas__name'],
                'value': item['value']
            }
            for item in data
        ]

        self.data['gases_emitted_by_scope'] = summary
        return summary

    def gases_emitted_by_scope_and_source_type(self):
        data = self.gases_emitted_by_factor.values(
            'activity__emission_source__group__category__scope__name',
            'activity__emission_source__source_type__name',
            'greenhouse_gas__name'
        ).annotate(
            value=Sum('value')
        ).order_by(
            'activity__emission_source__group__category__scope__name',
            'activity__emission_source__source_type__name',
            'greenhouse_gas__name'
        )

        summary = [
            {
                'scope': item['activity__emission_source__group__category__scope__name'],
                'source_type': item['activity__emission_source__source_type__name'],
                'gas_name': item['greenhouse_gas__name'],
                'value': item['value']
            }
            for item in data
        ]

        self.data['gases_emitted_by_scope_and_source_type'] = summary
        return summary

    def gases_emitted_by_group(self):
        data = self.gases_emitted_by_factor.values(
            'activity__emission_source__group__name', 'greenhouse_gas__name'
        ).annotate(
            value=Sum('value')
        ).order_by('activity__emission_source__group__name', 'greenhouse_gas__name')

        summary = [
            {
                'group': item['activity__emission_source__group__name'],
                'gas_name': item['greenhouse_gas__name'],
                'value': item['value']
            }
            for item in data
        ]

        self.data['gases_emitted_by_group'] = summary
        return summary

    def queryset(self):
        filters = {
            'location__company': self.company
        }
        if self.location_id is not None:
            filters['location_id'] = self.location_id
        if self.category_id is not None:
            filters['emission_source__group__category_id'] = self.category_id
        if self.scope_id is not None:
            filters['emission_source__group__category__scope_id'] = self.scope_id
        if self.group_id is not None:
            filters['emission_source__group__id'] = self.group_id
        if self.source_type_id is not None:
            filters['emission_source__source_type_id'] = self.source_type_id
        if self.emission_source_id is not None:
            filters['emission_source__id'] = self.emission_source_id
        if self.factor_type_id is not None:
            filters['emission_source__factor_type_id'] = self.factor_type_id
        if self.factor_id is not None:
            filters['emission_source__emission_factor__id'] = self.factor_id
        if self.initial_date is not None:
            initial_date = datetime.strptime(self.initial_date, '%Y-%m-%d')
            filters['year__gte'] = initial_date.year
            filters['month__gte'] = initial_date.month
        if self.end_date is not None:
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            filters['year__lte'] = end_date.year
            filters['month__lte'] = end_date.month
        if self.year:
            filters['year'] = self.year
        if self.month:
            filters['month'] = self.month

        # Filter by activities
        self.filtered_activities = Activity.objects.filter(**filters).select_related(
            'location',
            'emission_source__group__category',
            'emission_source__source_type',
            'emission_source__factor_type'
        ).prefetch_related(
            Prefetch('gases_emitted_by_factor', queryset=ActivityGasEmittedByFactor.objects.select_related(
                'emission_factor', 'greenhouse_gas'
            ))
        )

        # Prefetch gases emitidos por factor
        self.gases_emitted_by_factor = ActivityGasEmittedByFactor.objects.filter(
            activity__in=self.filtered_activities
        ).select_related(
            'emission_factor',
            'greenhouse_gas'
        )

        return self.filtered_activities

    def calculate(self):
        # Filter data by attributes set's
        self.queryset()
        self.data['activities_filtered'] = self.filtered_activities

        # Calculate data summaries
        self.emissions_by_source_type_and_scope()
        self.emissions_by_source_type_and_scope()
        self.emissions_by_scope()
        self.emissions_direct_and_indirect()
        self.gases_emitted_by_scope()
        self.gases_emitted_by_scope_and_source_type()
        self.gases_emitted_by_group()
        self.emissions_by_gas(),
        self.emissions_by_source(),
        self.emissions_by_classification_group(),
        self.get_total_co2e()
        return self.data
