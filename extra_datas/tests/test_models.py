from django.test import TestCase

from uuid import uuid4

from users.tests.mocks import mock_user
from users.models import User
from books.tests.mocks import mock_book
from books.models import Book
from extra_datas.models import Extra_Data

from .mock import mock_extra_data


class Extra_DataModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = mock_user
        cls.book_data = mock_book
        cls.extra_data_data = mock_extra_data

        cls.user = User.objects.create_user(**cls.user_data)
        cls.book = Book.objects.create(**cls.book_data, user=cls.user)
        cls.extra_data = Extra_Data.objects.create(
            **{**cls.extra_data_data, "book": cls.book}
        )

    def test_extra_data_model(self):
        extra_data = Extra_Data.objects.get(id=self.extra_data.id)

        id = extra_data._meta.get_field("id")
        translater = extra_data._meta.get_field("translater")
        translated = extra_data._meta.get_field("translated")
        additional_data = extra_data._meta.get_field("additional_data")

        self.assertIsInstance(extra_data, Extra_Data)
        self.assertEqual(extra_data, self.extra_data)

        self.assertIsNotNone(id)
        self.assertEqual(id.default, uuid4)
        self.assertTrue(id.primary_key)
        self.assertFalse(id.editable)

        self.assertEqual(translater.max_length, 100)
        self.assertTrue(translater.null)
        self.assertTrue(translater.blank)

        self.assertFalse(translated.null)
        self.assertFalse(translated.blank)
        self.assertFalse(translated.default)

        self.assertIsNone(additional_data.default)
        self.assertTrue(additional_data.null)
        self.assertTrue(additional_data.blank)

        self.assertIsInstance(extra_data.book, Book)
        self.assertTrue(extra_data.book, self.book)