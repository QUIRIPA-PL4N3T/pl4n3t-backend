from django.utils.translation import activate
from django.conf import settings
from django.shortcuts import render, redirect
from main.models import WebinarRegistrant
from django.contrib import messages
from django.utils.translation import gettext as _


def home(request):
    return render(request, 'home.html')


def blog(request):
    return render(request, 'blog.html')


def company(request):
    return render(request, 'company.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def why_quantify(request):
    return render(request, 'why_quantify.html')


def carbon_footprint(request):
    return render(request, 'carbon_footprint.html')


def plastic_footprint(request):
    return render(request, 'plastic_footprint.html')


def water_footprint(request):
    return render(request, 'water_footprint.html')


def footprint_levels(request):
    return render(request, 'footprint_levels.html')


def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in dict(settings.LANGUAGES):
            activate(language)
    return redirect(request.META.get('HTTP_REFERER'))


def webinar_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        company_name = request.POST.get('company_name', '')
        if WebinarRegistrant.objects.filter(email=email).exists():
            messages.info(request, _('This email is already registered.'))
        else:
            WebinarRegistrant.objects.create(email=email, company_name=company_name)
            messages.success(request, _('You have been successfully registered.'))
        return redirect('webinar')

    return render(request, 'blog.html')
