from location.location import Location


def location(request):
    return {'location': Location(request)}
