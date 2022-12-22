from django.test import TestCase

from uuid import uuid4

from users.models import User

from .mocks import mock_user


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = mock_user

        cls.user = User.objects.create_user(**cls.user_data)

    def test_user_model(self):
        user = User.objects.get(id=self.user.id)

        id = user._meta.get_field("id")
        username = user._meta.get_field("username")
        avatar = user._meta.get_field("avatar")
        email = user._meta.get_field("email")
        birth = user._meta.get_field("birth")
        stars = user._meta.get_field("stars")

        self.assertIsInstance(user, User)
        self.assertEqual(user, self.user)

        self.assertIsNotNone(id)
        self.assertEqual(id.default, uuid4)
        self.assertTrue(id.primary_key)
        self.assertFalse(id.editable)

        self.assertTrue(username.unique)
        self.assertTrue(username.max_length, 150)

        self.assertTrue(avatar.null)
        self.assertTrue(avatar.blank)
        self.assertEqual(avatar.default, None)

        self.assertFalse(email.unique)
        self.assertFalse(email.null)
        self.assertFalse(email.blank)

        self.assertFalse(birth.unique)
        self.assertFalse(birth.null)
        self.assertFalse(birth.blank)

        self.assertEqual(stars.default, 5)
        self.assertFalse(stars.editable)
