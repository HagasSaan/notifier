from rest_framework import viewsets, permissions

from .models import ConsumerModel, CustomConsumer
from .serializers import ConsumerModelSerializer, CustomConsumerSerializer


class ConsumerModelViewSet(viewsets.ModelViewSet):
    queryset = ConsumerModel.objects.all()
    serializer_class = ConsumerModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomConsumerViewSet(viewsets.ModelViewSet):
    queryset = CustomConsumer.objects.all()
    serializer_class = CustomConsumerSerializer
    permission_classes = [permissions.IsAuthenticated]
