from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_links


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    link_video = serializers.CharField(
        validators=[validate_links], required=False, allow_blank=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_of_same_course = SerializerMethodField()
    lessons_of_same_course = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def get_count_lesson_of_same_course(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_lessons_of_same_course(self, obj):
        lessons = Lesson.objects.filter(course=obj)
        return LessonSerializer(lessons, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "count_lesson_of_same_course",
            "lessons_of_same_course",
            "is_subscribed",
        )
