import graphene

from configuration.schema import ConfigurationsQuery
from message_consumers.schema import ConsumerModelsQuery
from message_producers.schema import ProducerModelsQuery


class Query(
    ConfigurationsQuery,
    ConsumerModelsQuery,
    ProducerModelsQuery,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query)
