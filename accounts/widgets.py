from django import forms


class CustomSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, *args, **kwargs):
        a = '<div id="custom_select" style="height:100px; overflow-y: scroll; border: 2px solid #ccc; ' \
            'border-radius: 5px; list-style: none;">'
        select = super().render(*args, **kwargs)
        return a + select + '</div>'
