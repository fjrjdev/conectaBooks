from django.test import TestCase

from uuid import uuid4

from genders.models import Gender

from .mock import mock_gender


class GenderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.gender_data = mock_gender

        cls.gender = Gender.objects.create(**cls.gender_data)

    def test_gender_model(self):
        gender = Gender.objects.get(id=self.gender.id)

        id = gender._meta.get_field("id")
        genders = gender._meta.get_field("genders")
        
        self.assertIsInstance(gender, Gender)
        self.assertEqual(gender, self.gender)
        
        self.assertIsNotNone(id)
        self.assertEqual(id.default, uuid4)
        self.assertTrue(id.primary_key)
        self.assertFalse(id.editable)
        
        self.assertEqual(genders.max_length, 100)
        self.assertFalse(genders.null)
        self.assertFalse(genders.blank)
        self.assertTrue(genders.default, "NONE")