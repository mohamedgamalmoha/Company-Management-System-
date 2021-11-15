from decimal import Decimal, ROUND_UP
from django.http.response import HttpResponseNotAllowed


def decimal_limit(func):
    def inner(*args, **kwargs):
        return Decimal(func(*args, **kwargs)).quantize(Decimal('.01'), rounding=ROUND_UP)
    return inner


def ajax_get_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.is_ajax() and request.method == "GET":
            return view_func(request, *args, **kwargs)
        return HttpResponseNotAllowed
    return wrapper_func

