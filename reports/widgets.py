from datetime import date
from django import forms

from affairs.utils import MONTHS_NAMES


class DateSelectMonthYearWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        months = MONTHS_NAMES
        years = [(year, year) for year in [2018, 2019, 2020]]
        widgets = [
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.month, value.year]
        elif isinstance(value, str):
            year, month = value.split('-')
            return [month, year]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        month, year = super().value_from_datadict(data, files, name)
        return '{}-{}'.format(year, month)
