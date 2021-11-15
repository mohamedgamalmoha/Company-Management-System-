from django import forms


class CustomCheckboxInput(forms.CheckboxInput):
    def render(self, *args, **kwargs):
        return '<div class="custom-control custom-checkbox">' + super().render(*args, **kwargs) + '</div>'
