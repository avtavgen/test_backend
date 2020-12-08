import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Category, Content, ApiUser


class ContentModelTest(TestCase):
    """ Test module for api """

    def setUp(self):
        self.client = APIClient()

        self.user_1, _ = User.objects.get_or_create(username="test_user_1", password="test_password_1")
        self.user_2, _ = User.objects.get_or_create(username="test_user_2", password="test_password_2")

        self.user_1.apiuser.is_premium = True
        self.user_1.save()
        self.user_2.apiuser.is_premium = False
        self.user_2.save()

        test_category, _ = Category.objects.get_or_create(name="test category")
        test_content_1, _ = Content.objects.get_or_create(title="test title", preview_path="/", file_path="/",
                                                          description="test", is_premium=False)
        test_content_2, _ = Content.objects.get_or_create(title="test title2", preview_path="/", file_path="/",
                                                          description="test2", is_premium=True)
        test_content_1.categories.add(test_category)
        test_content_2.categories.add(test_category)

    def test_premium(self):
        self.client.force_authenticate(self.user_1)
        response = self.client.get(reverse("content"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]["is_premium"], True)

    def test_other(self):
        self.client.force_authenticate(self.user_2)
        response = self.client.get(reverse("content"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]["is_premium"], False)
