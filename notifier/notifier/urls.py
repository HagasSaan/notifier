from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import routers

from configuration.views import ConfigurationViewSet, UserViewSet
from message_consumers.views import CustomConsumerViewSet, ConsumerModelViewSet
from message_producers.views import CustomProducerViewSet, ProducerModelViewSet

router = routers.DefaultRouter()
router.register(r'configurations', ConfigurationViewSet)
router.register(r'users', UserViewSet)
router.register(r'custom_consumers', CustomConsumerViewSet)
router.register(r'consumer_models', ConsumerModelViewSet)
router.register(r'custom_producers', CustomProducerViewSet)
router.register(r'producer_models', ProducerModelViewSet)


urlpatterns = [
    path('', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=settings.USE_GRAPHIQL_INTERFACE))),
    path('restapi/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
