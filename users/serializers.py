from rest_framework.serializers import ModelSerializer

from users.models import Payments


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'