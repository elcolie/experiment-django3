from django.db.models import F
from django_filters import rest_framework as filters, OrderingFilter
from rest_framework import viewsets

from experiment_django3.insurances.api.serializers import PremiumSerializer, CalculatedPremiumSerializer
from experiment_django3.insurances.models import Premium


class PremiumFilter(filters.FilterSet):
    premium = filters.NumberFilter(label='premium', method='filter_premium')

    order_by = OrderingFilter(
        fields=(
            ('percentage', 'percentage'),
            ('sum_insured', 'sum_insured'),
            ('premium', 'premium'),
        )
    )

    class Meta:
        model = Premium
        fields = [
            'percentage',
            'premium',
        ]

    def filter_premium(self, queryset, name, value):
        if name == 'premium':
            return queryset.filter(premium__gte=value)
        else:
            return queryset


class PremiumViewSet(viewsets.ModelViewSet):
    """
    premium = percentage * sum_insured(given by Frontend)
    """
    permission_classes = ()
    queryset = Premium.objects.all()
    serializer_class = PremiumSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PremiumFilter

    def get_serializer_class(self):
        """
        Show 2 use cases
        1. Ordinary lookup `serializer`
        2. Filter on `calculated field` serializer
        :return:
        """
        # GET with payload `sum_insured` will filter on `calculated field`
        if self.request.method == 'GET' and self.request.query_params.get('sum_insured') is not None:
            return CalculatedPremiumSerializer
        else:
            # else use normal lookup `serializer`
            return self.serializer_class

    def get_queryset(self):
        """
        User has 2 logic to do query
        1. lookup
        2. lookup on `calculated premium` field
        :return:
        """
        # Annotate to get `calculated premium` and filter it with given `sum_insured`
        given_sum_insured = self.request.query_params.get('sum_insured')
        if self.request.method == 'GET' and given_sum_insured is not None:
            return self.queryset.annotate(
                premium=F('percentage') / 100.0 * given_sum_insured
            )
        else:
            return self.queryset
