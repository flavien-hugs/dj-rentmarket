import random
from core import settings
from location.models import LocationModel
from shop.models import ProductModel, MainCategoryModel, CategoryModel


def meta(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_desc': settings.SITE_DESCRIPTION,
        'meta_keyw': settings.META_KEYWORDS,
        'request': request
    }


def location(request):
    location_obj, new_obj = LocationModel.objects.new_or_get(request)
    return {'location': location_obj}


# mélange la séquence x
def category(request):
    return {
        'category': CategoryModel.objects.all(),
        'scategory': MainCategoryModel.objects.all(),
        'main_category': sorted(
            MainCategoryModel.objects.all()[:6],
            key=lambda x: random.random())
    }


def featured_product(request):
    featured_product = sorted(ProductModel.objects.featured().filter(
       pub_date__isnull=False).order_by('-pub_date')[:50],
        key=lambda x: random.random())

    return {'featured_product': featured_product}


def get_info_ur(request):
    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""

    if request.user_agent.is_mobile:
        device_type = 'Mobile'
    if request.user_agent.is_tablet:
        device_type = 'Tablet'
    if request.user_agent.is_pc:
        device_type = 'PC'
    if request.user_agent.is_touch_capable:
        device_type = 'touch capable'
    if request.user_agent.is_bot:
        device_type = 'bot'

    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string

    device_family = request.user_agent.device.family

    context = {
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type": os_type,
        "os_version": os_version,
        "device_family": device_family
    }

    return context
