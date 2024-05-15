from datetime import datetime, timedelta
import mercadopago
from django.conf import settings
from rest_framework import viewsets, mixins, permissions, status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from memberships.models import Membership, CompanyMembership
from memberships.serializers import MembershipSerializer, CompanyMembershipSerializer, PurchaseMemberSerializer


@extend_schema(tags=['Memberships'])
class MembershipViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


@extend_schema(tags=['Memberships'])
class CompanyMembershipViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = CompanyMembership.objects.all()
    serializer_class = CompanyMembershipSerializer

    def get_queryset(self):
        user = self.request.user
        return CompanyMembership.objects.filter(company__members_roles__user=user)


@extend_schema(tags=['Memberships'])
class PurchaseMembershipView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        description=_("Compra una membresía"),
        request=PurchaseMemberSerializer,
        methods=["post"],
        responses={
            200: OpenApiResponse(description=_('Compra de membresía exitosa')),
            401: OpenApiResponse(description=_('No tiene permiso para ver este usuario')),
            400: OpenApiResponse(description=_('Solicitud incorrecta')),
        },
    )
    def post(self, request, membership_id):
        serializer = PurchaseMemberSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            membership = Membership.objects.get(id=membership_id)
            user = request.user

            mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

            preference_data = {
                "items": [
                    {
                        "title": membership.name,
                        "quantity": 1,
                        "unit_price": float(membership.price),
                    }
                ],
                "payer": {
                    "email": user.email,
                },
                "back_urls": {
                    "success": "http://www.your-site.com/membership/success",
                    "failure": "http://www.your-site.com/membership/failure",
                    "pending": "http://www.your-site.com/membership/pending"
                },
                "auto_return": "approved",
            }

            preference_response = mp.preference().create(preference_data)
            preference = preference_response["response"]

            # Guardar la preferencia en la sesión del usuario para futura verificación
            request.session['preference_id'] = preference["id"]

            return Response(
                {'init_point': preference["init_point"]},
                status=status.HTTP_200_OK
            )
        except Membership.DoesNotExist:
            return Response(
                {'detail': 'Membership not found'},
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
        methods=["get"],
        responses={
            200: OpenApiResponse(description=_('Membresía asignada exitosamente')),
            400: OpenApiResponse(description=_('Solicitud incorrecta')),
        },
    )
    def get(self, request):
        try:
            preference_id = request.session.get('preference_id')
            if not preference_id:
                return Response({'detail': _('No preference ID found in session')}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar el estado del pago
            mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            payment_status = mp.payment().get(preference_id)

            if payment_status['status'] == 'approved':
                # Obtener la membresía y la compañía
                user = request.user
                company = user.company
                membership_id = payment_status['response']['items'][0]['id']
                membership = Membership.objects.get(id=membership_id)

                # Asignar la membresía a la compañía
                CompanyMembership.objects.create(
                    company=company,
                    membership=membership,
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(days=membership.duration)
                )

                return Response(
                    data={'detail': 'Membership assigned successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={'detail': 'Payment not approved'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            exception_message = str(e)
            return Response(
                data={'detail': exception_message},
                status=status.HTTP_400_BAD_REQUEST
            )
