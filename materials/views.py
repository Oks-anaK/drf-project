from datetime import timedelta

from django.utils import timezone
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from materials.tasks import send_info_about_updates
from users.permissions import IsModerator, IsNotModeratorAndOwner, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """Фильтрация: модераторы видят все, обычные пользователи - только свои курсы."""
        # Проверка для генерации схемы Swagger
        if getattr(self, "swagger_fake_view", False):
            return Course.objects.none()

        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()

        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in ["list", "retrieve", "update"]:
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner)
        elif self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModerator)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsNotModeratorAndOwner)
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.instance

        four_hours_ago = timezone.now() - timedelta(hours=4)
        should_send_notification = (
            not course.last_updated or course.last_updated < four_hours_ago
        )

        course = serializer.save()

        if should_send_notification:
            subscribers = Subscription.objects.filter(course=course)

            for subscription in subscribers:
                if subscription.user and subscription.user.email:
                    send_info_about_updates.delay(subscription.user.email, course.id)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CustomPagination

    def get_queryset(self):
        """Фильтрация: модераторы видят все, обычные пользователи - только свои уроки."""
        # Проверка для генерации схемы Swagger
        if getattr(self, "swagger_fake_view", False):
            return Lesson.objects.none()

        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()

        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        """Фильтрация: модераторы видят все, обычные пользователи - только свои уроки."""
        # Проверка для генерации схемы Swagger
        if getattr(self, "swagger_fake_view", False):
            return Lesson.objects.none()

        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()

        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        """Фильтрация: модераторы видят все, обычные пользователи - только свои уроки."""
        # Проверка для генерации схемы Swagger
        if getattr(self, "swagger_fake_view", False):
            return Lesson.objects.none()

        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()

        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_update(self, serializer):
        lesson = serializer.save()
        course = lesson.course

        four_hours_ago = timezone.now() - timedelta(hours=4)

        if not course.last_updated or course.last_updated < four_hours_ago:
            course.last_updated = timezone.now()
            course.save(update_fields=["last_updated"])

            subscribers = Subscription.objects.filter(course=course)

            for subscription in subscribers:
                if subscription.user and subscription.user.email:
                    send_info_about_updates.delay(subscription.user.email, course.id)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModeratorAndOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        # Возвращаем ответ в API
        return Response({"message": message})
