from decimal import Decimal, ROUND_UP
from django.http.response import HttpResponseNotAllowed
import warnings
from typing import Callable, Any
from functools import wraps, partial


def debug(func: Callable = None, *, prefix: str = '', log_info: bool = True) -> Any:
    """Execute function in debug mode. When it throws an error, it ignores and print the error"""

    if func is None:
        return partial(debug, prefix=prefix, log_info=log_info)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            if log_info:
                warnings.warn(f'{prefix} Function {func.__name__} \t Invoked Unsuccessfully  \t Error: {e}')
        else:
            return result
    return wrapper


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

