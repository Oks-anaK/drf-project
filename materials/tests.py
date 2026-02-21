from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Психосоматика")
        self.lesson = Lesson.objects.create(
            name="Миф или правда", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        # print(response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Миф или правда")

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {"name": "Лечение тревоги", "course": 1}
        response = self.client.post(url, data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "Лечение тревоги",
        }
        response = self.client.patch(url, data)
        # print(response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Лечение тревоги")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link_video": None,
                    "name": self.lesson.name,
                    "description": None,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(name="Психосоматика", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_sub_create(self):
        url = reverse("materials:subscriptions")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "подписка добавлена")

    def test_sub_delete(self):
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("materials:subscriptions")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "подписка удалена")
        self.assertEqual(Subscription.objects.all().count(), 0)

    def test_sub_invalid_course(self):
        url = reverse("materials:subscriptions")
        data = {"course_id": 99999}  # несуществующий курс
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
