from rest_framework import serializers

from experiment_django3.insurances.models import Premium


class PremiumSerializer(serializers.ModelSerializer):
    """
    For common `lookup` case
    """

    class Meta:
        model = Premium
        fields = [
            'percentage',
            'sum_insured',
        ]


class CalculatedPremiumSerializer(serializers.ModelSerializer):
    """
    For `calculated premium` lookup case
    """
    premium = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Premium
        fields = [
            'percentage',
            'premium',
        ]
        read_only_fields = ['percentage']
