from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from experiment_django3.insurances.api.viewsets import PremiumViewSet
from experiment_django3.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("insurances", PremiumViewSet)

app_name = "api"
urlpatterns = router.urls
