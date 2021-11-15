import datetime

from django import forms
from django.utils import datetime_safe
from django.utils.dates import MONTHS
from django.utils.formats import get_format
from django.utils.regex_helper import _lazy_re_compile


class CustomChoiceField(forms.ChoiceField):
    def validate(self, value):
        """Validate that the input is in self.choices."""
        super().validate(value)

    def valid_value(self, value):
        """Check to see if the provided value is a valid choice."""
        return True


class SelectMonthYearWidget(forms.Widget):
    none_value = ('', '---------')
    month_field = '%s_month'
    year_field = '%s_year'
    template_name = 'django/forms/widgets/select_date.html'
    input_type = 'select'
    select_widget = forms.Select
    date_re = _lazy_re_compile(r'(\d{4}|0)-(\d\d?)-(\d\d?)$')

    def __init__(self, attrs=None, years=None, months=None, empty_label=None):
        self.attrs = attrs or {}

        # Optional list or tuple of years to use in the "year" select box.
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 10)

        # Optional dict of months to use in the "month" select box.
        self.months = months or MONTHS
        # Optional string, list, or tuple to use as empty_label.
        if isinstance(empty_label, (list, tuple)):
            if len(empty_label) != 3:
                raise ValueError('empty_label list/tuple must have 3 elements.')

            self.year_none_value = ('', empty_label[0])
            self.month_none_value = ('', empty_label[1])
        else:
            if empty_label is not None:
                self.none_value = ('', empty_label)

            self.year_none_value = self.none_value
            self.month_none_value = self.none_value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        date_context = {}
        year_choices = [(i, str(i)) for i in self.years]
        if not self.is_required:
            year_choices.insert(0, self.year_none_value)
        year_name = self.year_field % name
        date_context['year'] = self.select_widget(attrs, choices=year_choices).get_context(
            name=year_name,
            value=context['widget']['value']['year'],
            attrs={**context['widget']['attrs'], 'id': 'id_%s' % year_name},
        )
        month_choices = list(self.months.items())
        if not self.is_required:
            month_choices.insert(0, self.month_none_value)
        month_name = self.month_field % name
        date_context['month'] = self.select_widget(attrs, choices=month_choices).get_context(
            name=month_name,
            value=context['widget']['value']['month'],
            attrs={**context['widget']['attrs'], 'id': 'id_%s' % month_name},
        )
        subwidgets = [
            date_context[field]['widget'] for field in self._parse_date_fmt()
        ]

        context['widget']['subwidgets'] = subwidgets
        return context

    def format_value(self, value):
        """
        Return a dict containing the year, month, and day of the current value.
        Use dict instead of a datetime to allow invalid dates such as February
        31 to display correctly.
        """
        year, month = None, None
        if isinstance(value, (datetime.date, datetime.datetime)):
            year, month = value.year, value.month,
        elif isinstance(value, str):
            match = self.date_re.match(value)
            if match:
                # Convert any zeros in the date to empty strings to match the
                # empty option value.
                year, month = [int(val) or '' for val in match.groups()]
            else:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    d = datetime.datetime.strptime(value, input_format)
                except ValueError:
                    pass
                else:
                    year, month = d.year, d.month,
        return {'year': year, 'month': month}

    @staticmethod
    def _parse_date_fmt():
        fmt = get_format('DATE_FORMAT')
        escaped = False
        for char in fmt:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char in 'Yy':
                yield 'year'
            elif char in 'bEFMmNn':
                yield 'month'

    def id_for_label(self, id_):
        for first_select in self._parse_date_fmt():
            return '%s_%s' % (id_, first_select)
        return '%s_month' % id_

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == '':
            return None
        if y is not None and m is not None:
            input_format = get_format('DATE_INPUT_FORMATS')[0]
            try:
                date_value = datetime.date(int(y), int(m), int(0))
            except ValueError:
                return '%s-%s' % (y or 0, m or 0)
            date_value = datetime_safe.new_date(date_value)
            return date_value.strftime(input_format)
        return data.get(name)

    def value_omitted_from_data(self, data, files, name):
        return all(
            '{}_{}'.format(name, interval) not in data
            for interval in ('year', 'month')
        )
