from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from reports.models import ReportTemplate, CompanyTemplate, Report
from reports.serializers import (
    ReportTemplateListSerializer, ReportTemplateDetailSerializer,
    CompanyTemplateListSerializer, CompanyTemplateDetailSerializer,
    ReportListSerializer, ReportDetailSerializer
)
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from django.utils.translation import gettext_lazy as _


@extend_schema(tags=['Reports'])
class ReportTemplateViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateDetailSerializer

    @extend_schema(
        summary=_("Lista todas los plantillas de Pl4n3t"),
        responses={200: ReportTemplateListSerializer}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReportTemplateListSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Reports'])
class CompanyTemplateViewSet(viewsets.ModelViewSet):
    queryset = CompanyTemplate.objects.all()
    serializer_class = CompanyTemplateDetailSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        return queryset.filter(company__members_roles__user=user)

    @extend_schema(
        summary=_("Lista todos las plantillas de la compañía"),
        responses={200: CompanyTemplateListSerializer}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CompanyTemplateListSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Reports'])
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportDetailSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        return queryset.filter(company__members_roles__user=user)

    @extend_schema(
        summary=_("Lista todos los reportes"),
        responses={200: ReportListSerializer}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReportListSerializer(queryset, many=True)
        return Response(serializer.data)
