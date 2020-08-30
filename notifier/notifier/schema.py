import graphene

from configuration.models import Configuration
from configuration.schema import ConfigurationType
from message_consumers.models import ConsumerModel
from message_consumers.schema import ConsumerModelType
from message_producers.models import ProducerModel
from message_producers.schema import ProducerModelType


class Query(graphene.ObjectType):
    configurations = graphene.List(ConfigurationType)
    producer_models = graphene.List(ProducerModelType)
    consumer_models = graphene.List(ConsumerModelType)


    def resolve_configurations(root, info):
        return Configuration.objects.all()

    def resolve_producer_models(root, info):
        return ProducerModel.objects.all()

    def resolve_consumer_models(root, info):
        return ConsumerModel.objects.all()


schema = graphene.Schema(query=Query)
