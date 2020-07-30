import random
import cloudinary
from location.models import LocationModel
from shop.models import ProductModel, MainCategoryModel, CategoryModel


def consts(request):
    return dict(ICON_EFFECTS = dict(
        format="jgp",
        type="facebook",
        transformation=[
            dict(height=700, width=700,
                crop="thumb",
                gravity="face",
                effect="sepia"),
            dict(angle=10),
        ]
    ),

    THUMBNAIL = {
        "format": "jpg",
        "crop": "fill",
        "height": 150, "width": 150,
    },

    CLOUDINARY_CLOUD_NAME = cloudinary.config().cloud_name)


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
    context = {
        'featured_product': random.sample(featured_product, k=2)
    }
    return context


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
