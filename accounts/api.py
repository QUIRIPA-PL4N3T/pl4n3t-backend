import logging
from django.conf import settings
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import permissions, status, mixins, viewsets, parsers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests
from accounts.serializers import CustomTokenObtainPairSerializer, UserModelSerializer, RegisterSerializer, TokenOutput, \
    LogoutSerializer, ResetPasswordSerializer, ResetPasswordRequestSerializer, UserAvatarSerializer, \
    GoogleAccountSerializer, UpdatePasswordSerializer
import firebase_admin
from firebase_admin import auth, credentials


cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)


logger = logging.getLogger(__name__)


@extend_schema(tags=['Accounts'])
class UserDetailAPIView(GenericAPIView):
    """
    get:
    Get current user.
    This API resources use API View.
    post:
    Update current user.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=UserModelSerializer,
        summary=_("Obtiene la información de un usuario mediante el nombre usuario"),
        description=_("Obtiene la información de un usuario mediante el nombre usuario"),
        responses={
            200: UserModelSerializer,
            404: OpenApiResponse(description=_('El Usuario no existe')),
        },
        methods=["get"]
    )
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        request=UserModelSerializer,
        description=_("Actualiza los datos del usuario, solo el usuario puede actualizar sus datos"),
        responses={
            200: UserModelSerializer,
            404: OpenApiResponse(description=_('El Usuario no existe')),
            400: OpenApiResponse(description=_('Datos inválidos')),
            401: OpenApiResponse(description=_('Usted no tiene permiso para actualizar este usuario')),
        },
        methods=["post"]
    )
    def post(self, request, username):
        # Only can update yourself
        if request.user.username == username:
            user = get_object_or_404(User, username=username)
            serializer = UserModelSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': _("Usted no tiene permiso para actualizar este usuario")},
                            status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        request=UserModelSerializer,
        summary=_("Elimina un usuario, solo el usuario se puede eliminar a si mismo"),
        description=_("Elimina un usuario, solo el usuario se puede eliminar a si mismo"),
        responses={
            201: OpenApiResponse(description=_('Eliminación exitosa del usuario')),
            404: OpenApiResponse(description=_('El Usuario no existe')),
            400: OpenApiResponse(description=_('Usted no tiene permiso para eliminar este usuario')),
        },
        methods=["delete"]
    )
    def delete(self, request, username):
        # Only can delete yourself
        if request.user.username == username:
            user = get_object_or_404(User, pk=request.user.id)
            user.status = "DELETED"
            user.is_active = False
            user.save()
            return Response({"status": "OK"})
        else:
            return Response({'detail': _('Usted no tiene permiso para eliminar este usuario')},
                            status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class RegisterAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary=_("Registrar un nuevo Usuario"),
        description=_("Registrar un nuevo Usuario"),
        request=RegisterSerializer,
        responses={200: UserModelSerializer},
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        try:
            """
            Register a new user and return it's details
            """
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(UserModelSerializer(user).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_message = str(e)
            return Response({'detail': exception_message}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class ResetPasswordRequestAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    @extend_schema(
        summary=_("Recuperar Contraseña"),
        description=_("Solicitar el cambio de contraseña"),
        request=ResetPasswordRequestSerializer,
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                user.send_password_reset_email()
                return Response({
                    'detail': _('Se envió un correo con para continuar con la recuperación de la contraseña')},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response({'detail': _('No existe un usuario con este correo')},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class ResetPasswordConfirmAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    @extend_schema(
        summary=_("Cambiar contraseña con un token de recuperación"),
        description=_("Cambiar contraseña"),
        request=ResetPasswordSerializer,
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(activation_token=token)
            except User.DoesNotExist:
                return Response({
                    'error': _('El enlace de restablecimiento de contraseña no es válido.')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(password)
            user.activation_token = get_random_string(128)
            user.save()
            return Response(
                {'detail': _('Se ha completado la cambio de la contraseña Exitosamente')},
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class CurrentUserAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary=_("Obtiene el Usuario Actual utilizando el token en el HEADER"),
        description=_("Obtiene el Usuario Actual utilizando el token en el HEADER"),
        responses={
            200: UserModelSerializer,
            401: OpenApiResponse(description=_('Usted no tiene permiso para ver este usuario')),
        },
        methods=["get"]
    )
    def get(self, request):
        """
        Authenticate current user and return his/her details
        """
        current_user = UserModelSerializer(request.user, )
        logger.info(f"Authenticating current user {request.user.username}")

        return Response(current_user.data)

    @extend_schema(
        request=UserModelSerializer,
        summary=_("Actualiza el Usuario Actual utilizando el token en el HEADER"),
        description=_("Actualiza los datos del usuario, solo el usuario puede actualizar sus datos"),
        responses={
            200: UserModelSerializer,
            404: OpenApiResponse(description=_('El Usuario no existe')),
            400: OpenApiResponse(description=_('Datos inválidos')),
            401: OpenApiResponse(description=_('Usted no tiene permiso para actualizar este usuario')),
        },
        methods=["post"]
    )
    def post(self, request):
        user = request.user
        serializer = UserModelSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class UpdatePasswordAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    @extend_schema(
        summary=_("Actualizar contraseña del usuario"),
        description=_("Actualizar contraseña del usuario"),
        request=UpdatePasswordSerializer,
        methods=["post"]
    )
    def post(self, request):
        user = request.user
        serializer = UpdatePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description=_("Cerrar sesión"),
        request=LogoutSerializer,
        methods=["post"],
        responses={
            200: OpenApiResponse(description=_('Cierre de sesión exitoso')),
            401: OpenApiResponse(description=_('Usted no tiene permiso para ver este usuario')),
        },
    )
    def post(self, request, *args, **kwargs):
        try:            
            refresh_token = RefreshToken.for_user(request.user)
            refresh_token.blacklist()

            return Response({'detail': _('Sesión cerrada correctamente')}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class CustomObtainTokenPairWithView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        description=_("Iniciar Sesión"),
        responses={200: TokenOutput},
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['Accounts'])
class GoogleLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    @extend_schema(
        description=_("Iniciar sesión con una cuenta de google"),
        request=GoogleAccountSerializer,
        methods=["post"],
        responses={200: TokenOutput},
    )
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        try:
            decoded_token = google_id_token.verify_firebase_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            email = decoded_token['email']
            username = decoded_token['name']
            picture = decoded_token['picture']
            uid = decoded_token.get('uid')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'password': User.objects.make_random_password(),
                    'google_account': uid,
                    'google_picture': picture
                }
            )

            # Active user created
            if created:
                user.is_active = True
                user.save()

            # Update google picture
            if user.google_picture != picture:
                user.google_picture = picture
                user.save()

            if user.is_active:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response(data={
                    'access': access_token,
                    'refresh': refresh_token
                }, status=status.HTTP_200_OK
                )
            else:
                return Response(data={
                    'error': _('la cuenta de usuario no se encuentra activa')
                }, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Accounts'])
class AvatarViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserAvatarSerializer
    parser_classes = (
        parsers.MultiPartParser,
        parsers.FormParser,
        parsers.JSONParser,
    )

    @extend_schema(
        summary=_("Actualiza avatar del usuario"),
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'avatar': {
                        'type': 'string',
                        'format': 'binary'
                    },
                }
            }
        },
        # request=UserAvatarSerializer,
        responses={200: UserModelSerializer},
        methods=["post"]
    )
    @action(
        methods=['post'],
        detail=False,
    )
    def avatar(self, request):
        try:
            user = request.user
            serializer = self.get_serializer(data=request.data) # noqa
            if serializer.is_valid(raise_exception=True):
                user.avatar = serializer.validated_data['avatar']
                user.save()

                user_serializer = UserModelSerializer(user)
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_success_headers(self, data): # noqa
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
