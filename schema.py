import graphene

from experiment_django3.insurances.graphql.queries import Query


class Query(Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
