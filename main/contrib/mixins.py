"""
Basic building blocks for generic class based views.

We don't bind behaviour to http method handlers yet,
which allows mixin classes to be composed in interesting ways.
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from django.utils.translation import gettext_lazy as _


class UserCreateMixinViewSet:

    def get_user_queryset(self, model, query=None, trashed=False):
        if query is None:
            query = {}
        if self.request is None:
            return model.objects.none()
        user = self.request.user
        if hasattr(model, 'trashed'):
            query.update({'trashed': trashed})
        if user.is_agent:
            return model.objects.filter(**query)
        return model.objects.filter(user_created=user, **query)


class ListModelMixinWithRequest:
    """
    List a queryset send request data
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class RetrieveModelMixinWithRequest:
    """
    Retrieve a model instance send request data
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)


class CreateModelMixinWithRequest:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class UpdateModelMixinWithRequest:
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelOwnerMixin:
    """
    Destroy a model owner instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, 'can_delete') is False or instance.can_delete:
            if request.user.is_agent or (hasattr(instance, 'user_created') and request.user == instance.user_created):
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'error': _('usted no tiene permisos para eliminar este documento')},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(data={"delete": 'The instance cannot be deleted because of the status or because it is '
                                            'associated with another model.'})

    def perform_destroy(self, instance):
        instance.delete()
