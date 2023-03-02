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
    return render(request, 'why_quantify.html')


def carbon_footprint(request):
    return render(request, 'carbon_footprint.html')


def plastic_footprint(request):
    return render(request, 'plastic_footprint.html')


def water_footprint(request):
    return render(request, 'water_footprint.html')


def footprint_levels(request):
    return render(request, 'footprint_levels.html')
