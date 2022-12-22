from django.test import TestCase

from books.models import Book
from users.models import User
from extra_datas.models import Extra_Data

from users.tests.mocks import mock_user

from .mocks import mock_book, mock_extra_data

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book_data = mock_book
        cls.extra_data = mock_extra_data
        
        cls.user = User.objects.create(**mock_user)
        cls.book = Book.objects.create(
            **cls.book_data,
        user=cls.user
        )
        cls.extra = Extra_Data.objects.create(**{**cls.extra_data, "book":cls.book})

    def test_fields(self):
        self.assertEqual(
            self.book.title,
            self.book_data["title"]
        )
        self.assertEqual(
            self.book.transaction,
            self.book_data["transaction"]
        )
        self.assertEqual(
            self.book.price,
            self.book_data["price"]
        )
        self.assertEqual(
            self.book.available,
            self.book_data["available"]
        )
        self.assertEqual(
            self.book.author,
            self.book_data["author"]
        )
        self.assertEqual(
            self.book.year,
            self.book_data["year"]
        )
        self.assertEqual(
            self.book.publishing,
            self.book_data["publishing"]
        )
        self.assertEqual(
            self.book.condition,
            self.book_data["condition"]
        )
        self.assertEqual(
            self.book.isbn,
            self.book_data["isbn"]
        )

    def test_book_relations(self):
        self.assertTrue(self.book.extra_data.translated)
        self.assertEqual(
            self.book.user.username,
            mock_user["username"]
        )
