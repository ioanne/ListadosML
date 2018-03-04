from django import forms
from .models import Application


class SelectAppForm(forms.Form):
    application = forms.ModelChoiceField(
        label='application', queryset=Application.objects.all())
    application.widget.attrs.update({'class' : 'form-control'})
