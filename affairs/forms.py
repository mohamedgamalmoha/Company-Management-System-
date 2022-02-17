from django import forms
from django.forms.models import inlineformset_factory

from accounts.models import Worker
from reports.forms import BaseForm
from .widgets import CustomCheckboxInput
from .utils import MONTHS_NAMES, YEARS_NUMBERS
from .models import Month, Location, Activity, Vacations,  Day


class MonthUpdateForm(forms.ModelForm):

    class Meta:
        model = Month
        fields = ('worker', 'activity', 'month', 'year')
        labels = {
            'activity': 'النشاط',
            'worker': 'موظف'
        }
        widgets = {
            'worker': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'activity': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year':  forms.Select(attrs={'class': 'form-control'}),
        }


class MonthCreationForm(MonthUpdateForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label='الموقع',
                                      help_text='سيتم اضافة الموقع لكل يوم في الشهر تلقائيا',
                                      widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    def clean_location(self):
        location_id = self.cleaned_data.get('location')
        if location_id == "---------":
            raise forms.ValidationError('هذا الحقل مطلوب')
        return location_id


class MonthListFrom(BaseForm):
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                    label='العامل')
    activity = forms.ModelChoiceField(queryset=Activity.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='النشاط', required=False)
    month = forms.ChoiceField(choices=MONTHS_NAMES, label='الشهر', widget=forms.Select(attrs={'class': 'form-control'}),
                              required=False)
    year = forms.ChoiceField(choices=YEARS_NUMBERS, label='السنة', widget=forms.Select(attrs={'class': 'form-control'}),
                             required=False)


class ActivityCreationForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ActivityListForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='النشاط')


class LocationCreationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LocationListForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='الموقع')


class DayUpdateForm(forms.ModelForm):
    field_order = ['day_number', 'day_name', 'location', 'attendance', 'extra_work_hours', 'deduction', 'rewards', 'loans']
    day_name = forms.CharField(required=False, label="اليوم")

    def __init__(self, *args, **kwargs):
        super(DayUpdateForm, self).__init__(*args, **kwargs)
        day_name_field = self.fields.get('day_name')
        day_name_field.widget.attrs = {'class': 'form-control', 'readonly': True}
        day_name_field.initial = self.instance.get_day_name()

    class Meta:
        model = Day
        fields = '__all__'
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'attendance': CustomCheckboxInput(attrs={'class': 'custom-control-input'}),
            'day_number':  forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'style': "width: 50px"}),
            'extra_work_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'deduction': forms.NumberInput(attrs={'class': 'form-control'}),
            'rewards': forms.NumberInput(attrs={'class': 'form-control'}),
            'loans': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VacationsCreationForm(forms.ModelForm):

    class Meta:
        model = Vacations
        fields = '__all__'
        widgets = {
            'worker': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class VacationsListForm(forms.Form):
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), label='العامل')
    start_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control', 'type': 'date'}),
                                 label='من', required=False)
    end_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control', 'type': 'date'}),
                               label='الي', required=False)


MonthDaysInlineFormset = inlineformset_factory(Month, Day, form=DayUpdateForm, extra=0, can_delete=False)
