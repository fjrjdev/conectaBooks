from django.test import TestCase

from books.models import Book
from users.models import User
from extra_datas.models import Extra_Data

from users.tests.mocks import mock_user, mock_diff
from books.tests.mocks import mock_book, mock_extra_data

from borroweds.models import Borrowed

from .mocks import mock_borrowed


class BorrowedModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.book_data = mock_book
        cls.extra_data = mock_extra_data

        cls.owner = User.objects.create(**mock_user)
        cls.book = Book.objects.create(**cls.book_data, user=cls.owner)
        cls.extra = Extra_Data.objects.create(**{**cls.extra_data, "book": cls.book})

        cls.renter_data = mock_diff
        cls.renter = User.objects.create(**mock_diff)

        cls.borrowed_data = {
            **mock_borrowed,
            "book": cls.book,
            "user": cls.renter,
        }

        cls.borrowed = Borrowed.objects.create(**cls.borrowed_data)

    def test_fild_max_length(self):

        max_length = self.borrowed._meta.get_field("shipping_method").max_length
        self.assertEqual(max_length, 100)

    def test_borrowed_fields(self):
        self.assertIsNotNone(self.borrowed.id)
        self.assertEqual(
            self.borrowed.shipping_method, self.borrowed_data["shipping_method"]
        )
        self.assertIsNotNone(self.borrowed.initial_date)
        self.assertIsNone(self.borrowed.finish_date)

    def test_borrowed_foreign_keys(self):
        borrowed = Borrowed.objects.get(id=self.borrowed.id)

        self.assertIsInstance(borrowed.user, User)
        self.assertTrue(borrowed.user, self.renter)

        self.assertIsInstance(borrowed.book, Book)
        self.assertTrue(borrowed.book, self.book)
