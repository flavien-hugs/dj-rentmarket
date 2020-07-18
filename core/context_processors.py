from location.models import LocationModel
from shop.models import CategoryModel, ProductModel


def location(request):
    location_item, new_obj = LocationModel.objects.new_or_get(request)
    return {"location": location_item}


def category(request):
    nav = CategoryModel.objects.all()
    popular = ProductModel.objects.filter(available=True)

    return {'nav': nav, 'popular': popular}


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
