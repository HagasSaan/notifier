from django import forms

from .models import Configuration, User, MessageFilterModel


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class MessageFilterModelForm(forms.ModelForm):
    class Meta:
        model = MessageFilterModel
        fields = '__all__'
