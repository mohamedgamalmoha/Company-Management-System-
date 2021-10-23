from decimal import Decimal, ROUND_UP


def decimal_limit(func):
    def inner(*args, **kwargs):
        return Decimal(func(*args, **kwargs)).quantize(Decimal('.01'), rounding=ROUND_UP)
    return inner
