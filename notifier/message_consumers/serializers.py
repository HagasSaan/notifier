from rest_framework import serializers

from .models import ConsumerModel, CustomConsumer


class ConsumerModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConsumerModel
        fields = '__all__'


class CustomConsumerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomConsumer
        fields = '__all__'
