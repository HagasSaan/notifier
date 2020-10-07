from typing import Optional

from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Configuration, User
from .serializers import ConfigurationSerializer, UserSerializer
from .tasks import run_configuration as run_configuration_task


class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def run_configuration(self, request: Request, pk: Optional[str] = None):
        configuration = Configuration.objects.get(pk=pk)
        if settings.SYNC_MODE:
            configuration.run()
        else:
            run_configuration_task.delay(configuration.id)

        return Response({'status': 'success'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
