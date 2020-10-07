from rest_framework import serializers

from .models import Configuration, User


class ConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'status',
            'on_leave',
            'additional_info',
            'working_time_start',
            'working_time_end',
            'is_working_time',
        )
