from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_method', 'stripe_payment_url', 'stripe_session_id']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
