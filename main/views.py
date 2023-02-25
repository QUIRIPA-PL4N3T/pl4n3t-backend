from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def blog(request):
    return render(request, 'blog.html')


def company(request):
    return render(request, 'company.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def why_quantify(request):
    return render(request, 'contact_us.html')


def carbon_level(request):
    return render(request, 'carbon_level.html')
