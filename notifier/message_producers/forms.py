from django import forms

from .models import ProducerModel


class ProducerModelForm(forms.ModelForm):
    class Meta:
        model = ProducerModel
        fields = '__all__'
