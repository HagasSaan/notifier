from django import forms
from django_celery_beat.models import CrontabSchedule

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


class ScheduleConfigurationForm(forms.ModelForm):
    configuration = forms.ModelChoiceField(
        label='Configuration',
        queryset=Configuration.objects.all(),
        required=True,
    )

    class Meta:
        model = CrontabSchedule
        fields = '__all__'
