from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from users.models import Payments


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_of_same_course = SerializerMethodField()
    lessons_of_same_course = SerializerMethodField()

    def get_count_lesson_of_same_course(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_lessons_of_same_course(self, obj):
        lessons = Lesson.objects.filter(course=obj)
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = ("name", "description", "count_lesson_of_same_course", "lessons_of_same_course")
