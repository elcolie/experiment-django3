from django.contrib.auth import get_user_model
from django.db.models import F
from django.test import TransactionTestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from experiment_django3.insurances.models import Premium


class TestPremium(TransactionTestCase):
    def setUp(self) -> None:
        dummy = [
            Premium(percentage=1, sum_insured=(5000, None)),
            Premium(percentage=2, sum_insured=(6000, None)),
            Premium(percentage=3, sum_insured=(7000, None)),
            Premium(percentage=4, sum_insured=(10000, None)),
        ]
        Premium.objects.bulk_create(dummy)

    def test_filter(self):
        """
        FE would like to find the product that fit his bugdet(`premium`)
        `premium = percentage * sum_insured`
        This one need `annotate`
        :return:
        """
        given_sum_insured = 5000
        query = Premium.objects.annotate(premium=F('percentage') / 100.0 * given_sum_insured).values('percentage',
                                                                                                     'premium')
        '''
        SELECT insurances_premium.percentage,
                ((insurances_premium.percentage / 100.0) * 5000) AS premium
        FROM insurances_premium
        '''

        filtered_qs = query.filter(premium__gte=125)
        '''
        SELECT insurances_premium.percentage,
                ((insurances_premium.percentage / 100.0) * 5000) AS premium
        FROM insurances_premium
        WHERE ((insurances_premium.percentage / 100.0) * 5000) >= 125
        '''
        assert 4 == query.count()
        assert 2 == filtered_qs.count()

    def test_query_params(self):
        """
        Given `sum_insured` expect `response` only correct `premium`
        :return:
        """
        User = get_user_model()
        user = baker.make(User)
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('api:premium-list')
        data = {
            'sum_insured': 6000,
        }
        res = client.get(url, data=data)
        assert status.HTTP_200_OK == res.status_code
        assert res.data['results'][0]['premium'] == '60.00'
        assert res.data['results'][1]['premium'] == '120.00'
        assert res.data['results'][2]['premium'] == '180.00'
        assert res.data['results'][3]['premium'] == '240.00'
