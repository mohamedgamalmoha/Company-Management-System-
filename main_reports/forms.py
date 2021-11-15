from django import forms

from accounts.models import Worker
from affairs.models import Location
from accounts.widgets import CustomSelectMultiple
from affairs.utils import MONTHS_NAMES, YEARS_NUMBERS
from .widgets import SelectMonthYearWidget, CustomChoiceField


class BaseForm(forms.Form):
    UN_VALIDATED_FIELDS: tuple = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(
                field, (forms.ChoiceField, forms.Select)
            ) and not isinstance(field, forms.ModelChoiceField):
                field.choices = [("---------", "---------"), *field.choices]

    def add_error(self, field, error):
        if field not in self.UN_VALIDATED_FIELDS:
            super().add_error(field, error)


class WorkerBaseForm(BaseForm):
    UN_VALIDATED_FIELDS = ('start_date', 'end_date', 'location')
    location = forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='الموقع', required=False)
    start_date = CustomChoiceField(widget=SelectMonthYearWidget(attrs={'class': 'form-control'}),
                                   label='من', required=False)
    end_date = CustomChoiceField(widget=SelectMonthYearWidget(attrs={'class': 'form-control'}),
                                 label='الي', required=False)


class MultiWorkerForm(WorkerBaseForm):
    workers = forms.ModelMultipleChoiceField(queryset=Worker.objects.all(), widget=CustomSelectMultiple,
                                             label='العمال', required=True)


class SingleMonthForm(BaseForm):
    month = forms.ChoiceField(choices=MONTHS_NAMES, label='الشهر',  widget=forms.Select(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(choices=YEARS_NUMBERS, label='السنة',  widget=forms.Select(attrs={'class': 'form-control'}))
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                    label='العامل', required=True)


class AccommodationFrom(forms.Form):
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                      label='تاريخ انتهاء الجواز', required=False, help_text='سيتم عرض ما قبل التاريخ المحدد')
    qid_expiration_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
                                          , label='تاريخ انتهاء QID', required=False,  help_text='سيتم عرض ما قبل التاريخ المحدد')
