import requests
from django.shortcuts import render


def contact(request):
    is_cached = ('geodata' in request.session)
    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        response = requests.get('http://freegeoip.net/json/%s' % ip_address)
        request.session['geodata'] = response.json()
    geodata = request.session['geodata']
    template = 'pages/contact.html'
    context = {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'latitude': geodata['latitude'],
        'longitude': geodata['longitude'],
        'api_key': 'AIzaSyC1UpCQp9zHokhNOBK07AvZTiO09icwD8I',
        'is_cached': is_cached,
        'page_title': 'Contact Us',
    }
    return render(request, template, context)


def handler404(request):
    return render(request, 'pages/erreurs/404.html', status=404)


def handler500(request):
    return render(request, 'pages/erreurs/500.html', status=500)
