import json
import re

import graphene
from django.db.models import F
from django_filters import rest_framework as filters, OrderingFilter
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from experiment_django3.insurances.models import Premium
from experiment_django3.insurances.utils import extract_params


class PremiumGraphQLFilter(filters.FilterSet):
    """
    Hackish way to add `annotate` to `queryset`
    """
    premium = filters.NumberFilter(method='filter_premium')
    sum_insured = filters.NumberFilter(method='filter_sum_insured')
    order_by = OrderingFilter(
        fields=(
            ('percentage', 'percentage'),
            ('premium', 'premium'),
        )
    )

    class Meta:
        model = Premium
        fields = [
            'premium',
            'percentage',
            'sum_insured',
        ]

    def filter_premium(self, queryset, name, value):
        if name == 'premium':
            return queryset.filter(premium__gte=value)
        else:
            return queryset

    def filter_sum_insured(self, queryset, name, value):
        return queryset.filter(sum_insured__contains=value)


class PremiumNode(DjangoObjectType):
    sum_insured = graphene.String()
    premium = graphene.Float()

    class Meta:
        model = Premium
        fields = [
            'premium',
            'percentage',
            'sum_insured',
        ]
        interfaces = (relay.Node,)

    def resolve_premium(self, info):
        return self.premium

    @classmethod
    def get_queryset(cls, queryset, info):
        """
        If found `given_sum_insured` then do calculation on `premium`
        :param queryset:
        :param info:
        :return:
        """
        data = json.loads(info.context.body)
        input = re.search('\(([^)]+)', data['query']).group(1)
        my_dict = extract_params(input)
        qs = queryset.annotate(premium=F('percentage') / 100.0 * my_dict.get('sum_insured'))
        return qs


class Query:
    premium = relay.Node.Field(PremiumNode)
    all_premiums = DjangoFilterConnectionField(PremiumNode, filterset_class=PremiumGraphQLFilter)
