from django.urls import path, include
from rest_framework.routers import SimpleRouter
from users.views import PaymentViewSet

router = SimpleRouter()
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
]