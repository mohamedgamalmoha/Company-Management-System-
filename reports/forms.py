from django import forms
from django.contrib.auth.backends import get_user_model

from accounts.models import Worker
from affairs.models import Location
from affairs.utils import MONTHS_NAMES
from .widgets import DateSelectMonthYearWidget


User = get_user_model()

LOCATION_CHOICES = tuple((loc.name, loc.name) for loc in Location.objects.all())
NATIONALITY_CHOICES = tuple((worker.nationality, worker.nationality) for worker in Worker.objects.all())


class BaseReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.choices = [("---------", "---------"), *field.choices]


class SalaryRangeMonthReportForm(BaseReportForm):
    month_start = forms.ChoiceField(choices=MONTHS_NAMES, label='من')
    month_end = forms.ChoiceField(choices=MONTHS_NAMES, label='الي')


class LocationReportForm(BaseReportForm):
    month = forms.ChoiceField(choices=MONTHS_NAMES, label='الشهر')
    location = forms.ChoiceField(choices=LOCATION_CHOICES, label='الجنسية')


class ResidenceReportForm(BaseReportForm):
    date_start = forms.DateField(label='من', widget=DateSelectMonthYearWidget)
    date_end = forms.DateField(label='الي', widget=DateSelectMonthYearWidget)
