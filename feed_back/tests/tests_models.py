from django.test import TestCase
from uuid import uuid4

from users.models import User
from users.tests.mocks import mock_user, mock_diff

from books.models import Book
from books.tests.mocks import mock_book, mock_extra_data
from extra_datas.models import Extra_Data

from borroweds.models import Borrowed
from borroweds.test.mocks import mock_borrowed

from feed_back.models import FeedBack
from .mocks import mock_feed


class FeedBackModelTest(TestCase):
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
        cls.feed_back = FeedBack.objects.create(
            borrowed_id=cls.borrowed.id, **mock_feed
        )

    def test_fields(self):
        self.assertIsNotNone(self.feed_back.id)
        self.assertEqual(self.feed_back.stars_renter, mock_feed["stars_renter"])
        self.assertEqual(self.feed_back.stars_renter, mock_feed["rating_renter"])
        self.assertIsNone(self.feed_back.stars_owner)
        self.assertIsNone(self.feed_back.rating_owner)

    def test_relations(self):
        feed_back = FeedBack.objects.get(id=self.feed_back.id)
        self.assertIsInstance(feed_back.borrowed, Borrowed)
        self.assertTrue(feed_back.borrowed, self.borrowed)
