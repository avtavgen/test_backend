from django.test import TestCase

from api.models import Category, Content


class ContentModelTest(TestCase):
    """ Test module for Content model """

    def setUp(self):
        test_category, _ = Category.objects.get_or_create(name="test category")
        test_content_1, _ = Content.objects.get_or_create(title="test title", preview_path="/", file_path="/",
                                                          description="test", is_premium=False)
        test_content_2, _ = Content.objects.get_or_create(title="test title2", preview_path="/", file_path="/",
                                                          description="test2", is_premium=True)
        test_content_1.categories.add(test_category)
        test_content_2.categories.add(test_category)

    def test_model_str(self):
        test_content_1 = Content.objects.get(is_premium=False)
        test_content_2 = Content.objects.get(is_premium=True)
        self.assertEqual(str(test_content_1), "test title")
        self.assertEqual(str(test_content_2), "test title2")
