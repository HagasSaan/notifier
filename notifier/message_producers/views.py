from rest_framework import viewsets, permissions

from .models import ProducerModel, CustomProducer
from .serializers import ProducerModelSerializer, CustomProducerSerializer


class ProducerModelViewSet(viewsets.ModelViewSet):
    queryset = ProducerModel.objects.all()
    serializer_class = ProducerModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomProducerViewSet(viewsets.ModelViewSet):
    queryset = CustomProducer.objects.all()
    serializer_class = CustomProducerSerializer
    permission_classes = [permissions.IsAuthenticated]
