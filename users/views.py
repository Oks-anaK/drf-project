from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsUserOwner
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Добавить фильтры
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = "date_payment"
    ordering = "-date_payment"  # По умолчанию сортировка по дате (новые сначала)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.course:
            product_name = payment.course.name
        elif payment.lesson:
            product_name = payment.lesson.name
        else:
            product_name = "Payment"

        product = create_stripe_product(product_name)
        price = create_stripe_price(payment.amount, product.id)
        session_id, payment_link = create_stripe_session(price)
        payment.stripe_session_id = session_id
        payment.stripe_payment_url = payment_link
        payment.save()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)
