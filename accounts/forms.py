from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.backends import get_user_model

from .models import Worker
from .utlis import get_permissions_labels
from .widgets import CustomSelectMultiple


User = get_user_model()


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields.get('email').required = True

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['user_permissions'].choices = get_permissions_labels()

    class Meta:
        model = User
        fields = '__all__'
        exclude = ('groups', 'last_login', 'date_joined')
        widgets = {
            'user_permissions': CustomSelectMultiple,
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class WorkerCreationForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = '__all__'
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'qid': forms.TextInput(attrs={'class': 'form-control'}),
            'qid_expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guarantee': forms.TextInput(attrs={'class': 'form-control'}),
            'settlement_id': forms.TextInput(attrs={'class': 'form-control'}),
            'basic_salary': forms.TextInput(attrs={'class': 'form-control'}),
            'feeding_allowance': forms.TextInput(attrs={'class': 'form-control'}),
            'housing_allowance': forms.TextInput(attrs={'class': 'form-control'}),
            'transporting_allowance': forms.TextInput(attrs={'class': 'form-control'}),
        }


class WorkerListForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label='الاسم')


class UserListForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label='الاسم')
