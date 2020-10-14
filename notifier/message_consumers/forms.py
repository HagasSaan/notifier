from django import forms

from .models import ConsumerModel


class ConsumerModelForm(forms.ModelForm):
    class Meta:
        model = ConsumerModel
        fields = '__all__'
