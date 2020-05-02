import graphene
from django.db.models import F
from django_filters import rest_framework as filters, OrderingFilter
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from experiment_django3.insurances.api.viewsets import PremiumFilter
from experiment_django3.insurances.models import Premium


class PremiumGraphQLFilter(filters.FilterSet):
    """
    Hackish way to add `annotate` to `queryset`
    """
    order_by = OrderingFilter(
        fields=(
            ('percentage', 'percentage'),
        )
    )

    class Meta:
        model = Premium
        fields = [
            'percentage',
        ]

    # def filter_premium(self, queryset, name, value):
    #     if name == 'premium':
    #         return queryset.filter(premium__gte=value)
    #     else:
    #         return queryset


class PremiumNode(DjangoObjectType):
    sum_insured = graphene.String()
    premium = graphene.Float()

    class Meta:
        model = Premium
        filterset_class = PremiumFilter
        fields = [
            'premium',
            'percentage',
            'sum_insured',
        ]
        interfaces = (relay.Node,)

    def resolve_premium(self, info):
        return 200.12

    @classmethod
    def get_queryset(cls, queryset, info):
        """
        If found `given_sum_insured` then do calculation on `premium`
        :param queryset:
        :param info:
        :return:
        """

        qs = queryset.annotate(premium=F('percentage') * 2)
        # import ipdb;
        # ipdb.set_trace()
        return qs


class Query:
    premium = relay.Node.Field(PremiumNode)
    all_premiums = DjangoFilterConnectionField(PremiumNode)
