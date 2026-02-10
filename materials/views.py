from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """Фильтрация: модераторы видят все, обычные пользователи - только свои курсы."""
        queryset = super().get_queryset()
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
            self.permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)
        return super().get_permissions()


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

    def get_queryset(self):
        """Фильтрация: модераторы видят все, обычные пользователи - только свои уроки."""
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        """Фильтрация: модераторы видят все, обычные пользователи - только свои уроки."""
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        """Фильтрация: модераторы видят все, обычные пользователи - только свои уроки."""
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]
