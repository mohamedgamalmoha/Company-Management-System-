from django import forms

from .models import Month, Location


Activity_Choices = ((location.id, location.__str__()) for location in Location.objects.all())
Month_Activity_Choices = (("---------", "---------"), *Activity_Choices)


class MonthAddForm(forms.ModelForm):
    # location = forms.ChoiceField(choices=Month_Activity_Choices, label='الموقع', required=True,
    #                              help_text='سيتم اضافة الموقع لكل يوم في الشهر تلقائيا')
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label='الموقع', help_text='سيتم اضافة الموقع لكل يوم في الشهر تلقائيا')

    class Meta:
        model = Month
        fields = ('worker', 'activity', 'month', 'year', 'location')
        labels = {
            'activity': 'النشاط',
            'worker': 'موظف'
        }

    def clean_location(self):
        location_id = self.cleaned_data.get('location')
        if location_id == "---------":
            raise forms.ValidationError('هذا الحقل مطلوب')
        return location_id
