from rest_framework import serializers

from .models import ProducerModel, CustomProducer


class ProducerModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProducerModel
        fields = '__all__'


class CustomProducerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomProducer
        fields = '__all__'
