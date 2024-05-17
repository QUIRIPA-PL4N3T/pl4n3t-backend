from datetime import datetime, timedelta
import mercadopago
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from mercadopago import SDK
from rest_framework import viewsets, mixins, permissions, status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from companies.models import Company
from memberships.models import Membership, CompanyMembership
from memberships.serializers import MembershipSerializer, CompanyMembershipSerializer, PurchaseSerializer, \
    PreferenceResponseSerializer, PaymentVerificationSerializer


@extend_schema(tags=['Memberships'])
class MembershipViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


@extend_schema(tags=['Memberships'])
class CompanyMembershipViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = CompanyMembershipSerializer
    queryset = CompanyMembership.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Returns the membership for a specified company associated with the currently authenticated user.
        Requires the company ID to be specified in the URL parameters.
        """
        user = self.request.user
        company_id = self.kwargs.get('pk')  # Get company_id from URL parameters

        if not company_id:
            raise NotFound(_("el id de la compañía es requerido."))

        # Try to get the company membership for the specified company and check if the user is a member
        try:
            return CompanyMembership.objects.get(company__id=company_id, company__members_roles__user=user)
        except CompanyMembership.DoesNotExist:
            raise NotFound(_("No se han encontrado una membresía para la empresa y el usuario especificados."))


@extend_schema(tags=['Memberships'])
class PurchaseMembershipView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        description=_("Compra una membresía"),
        request=PurchaseSerializer,
        methods=["post"],
        responses={
            200: OpenApiResponse(response=PreferenceResponseSerializer, description=_('Compra de membresía exitosa')),
            401: OpenApiResponse(description=_('No tiene permiso para ver este usuario')),
            400: OpenApiResponse(description=_('Solicitud incorrecta')),
        },
    )
    def post(self, request, company_id, membership_id):
        serializer = PurchaseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            membership = Membership.objects.get(id=membership_id)
            company = Company.objects.get(id=company_id)

            # Validate membership price
            if membership.price <= 0:
                return Response(
                    {'detail': 'El precio de la membresía no es válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

            # Create payment preference data
            preference_data = {
                "items": [
                    {
                        "title": membership.name,
                        "quantity": 1,
                        "unit_price": int(membership.price)
                    }
                ],
                "payer": serializer.data["payer"],
                "back_urls": serializer.data["back_urls"],
                "auto_return": "approved",
            }

            # Create preference in MercadoPago
            preference_response = mp.preference().create(preference_data)
            preference = preference_response["response"]

            try:
                # Check if the company already has a membership
                company_membership = CompanyMembership.objects.get(company=company)
                # Update existing membership to Awaiting Payment status
                company_membership.proposed_membership = membership
                company_membership.proposed_end_date = timezone.now() + timedelta(days=membership.duration)
                company_membership.status = CompanyMembership.AWAITING_PAYMENT
                company_membership.save()
            except CompanyMembership.DoesNotExist:
                # Create new company membership if not exists
                CompanyMembership.objects.create(
                    company=company,
                    membership=membership,
                    start_date=timezone.now() + timedelta(days=1),  # Start date set to the next day
                    end_date=timezone.now() + timedelta(days=membership.duration),
                    # End date based on membership duration
                    status=CompanyMembership.AWAITING_PAYMENT  # Initial status set to awaiting payment
                )

            return Response(
                {'init_point': preference},
                status=status.HTTP_200_OK
            )
        except Membership.DoesNotExist:
            return Response(
                {'detail': 'Membership not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            exception_message = str(e)
            return Response(
                {'detail': exception_message},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=['Memberships'])
class MembershipPaymentSuccessView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        description=_("Verificación de pago de membresía exitosa"),
        request=PaymentVerificationSerializer,
        methods=["post"],
        responses={
            200: OpenApiResponse(description=_('Membresía asignada exitosamente')),
            400: OpenApiResponse(description=_('Solicitud incorrecta')),
        },
    )
    def post(self, request):
        user = request.user
        serializer = PaymentVerificationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(
                id=serializer.data['company_id'],
                members_roles__user=user
            )
        except Company.DoesNotExist:
            return Response({'detail': _('La compañía no existe')}, status=status.HTTP_404_NOT_FOUND)

        mp = SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        payment_status = mp.payment().get(serializer.data['preference_id'])

        if payment_status['status'] != 'approved':
            return Response({'detail': _('Payment not approved')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Get the membership
                membership_id = payment_status['response']['items'][0]['id']
                membership = Membership.objects.get(id=membership_id)
                company_membership = CompanyMembership.objects.get(company=company)

                # Set membership to the company
                company_membership.membership = membership
                company_membership.start_date = timezone.now() + timedelta(days=1)
                company_membership.end_date = timezone.now() + timedelta(days=membership.duration)
                company_membership.status = CompanyMembership.PAID
                company.save()

                return Response({'detail': _('Membership assigned successfully')}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
