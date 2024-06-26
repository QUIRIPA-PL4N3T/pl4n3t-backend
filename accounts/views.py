# views.py
import jwt
from django.conf import settings
from accounts.models import User
from django.shortcuts import render
from accounts.forms import UserPasswordResetForm


def activate_account(request):
    token = request.GET.get('reset_token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        user.is_active = True
        user.save()
        return render(request, 'account/activation_success.html')
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return render(request, 'account/invalid_token.html')


def password_reset_confirm(request):
    token = request.GET.get('reset_token')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return render(request, 'account/invalid_token.html')

    if request.method == 'POST':
        form = UserPasswordResetForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            user.is_active = True
            user.save()
            return render(request, 'account/password_reset_success.html')
        else:
            return render(
                request, 'account/password_reset_confirm.html',
                {
                    'form': form,
                    'error': form.errors
                }
            )
    return render(
        request, 'account/password_reset_confirm.html',
        {'form': UserPasswordResetForm(user)}
    )
