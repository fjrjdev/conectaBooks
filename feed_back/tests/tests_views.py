from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import User
from users.tests.mocks import (
    mock_user,
    mock_diff,
    mock_user_login,
    mock_user_diff_login,
)
from books.models import Book
from books.tests.mocks import mock_book, mock_extra_data, mock_genders


class FeedBackViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = mock_user
        cls.user_diff_data = mock_diff

        cls.book_data = mock_book
        cls.extra_data_data = mock_extra_data
        cls.gender_data = mock_genders

        cls.user_login = mock_user_login
        cls.user_diff_login = mock_user_diff_login

        cls.user = User.objects.create_user(**cls.user_data)
        cls.user_diff = User.objects.create_user(**cls.user_diff_data)

        cls.login = reverse("login")
        cls.base_url_book = reverse("book")

    def test_can_create_feedback(self):
        owner_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + owner_token.data["token"])

        book_response = self.client.post(
            self.base_url_book,
            {
                **self.book_data,
                "user": self.user_data,
                "extra_data": self.extra_data_data,
                "genders": self.gender_data,
            },
            format="json",
        )

        renter_token = self.client.post(self.login, self.user_diff_login, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + renter_token.data["token"]
        )

        response = self.client.post(
            f"/api/borrowed/{book_response.data['id']}/book/",
            {"shipping_method": "Retirada", "finish_date": "2023-01-01"},
            format="json",
        )
        response_feed = self.client.post(
            f"/api/feedback/{response.data['id']}/borrowed/",
            {"stars_renter": 5, "rating_renter": "Very Good"},
            format="json",
        )

        self.assertTrue(response_feed.status_code, 201)
        self.assertEqual(response_feed.data["stars_renter"], 5)
        self.assertEqual(response_feed.data["rating_renter"], "Very Good")
        self.assertEqual(response_feed.data["borrowed"]["id"], response.data["id"])

    def test_cant_create_feedback_if_not_owner_or_renter(self):
        owner_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + owner_token.data["token"])

        book_response = self.client.post(
            self.base_url_book,
            {
                **self.book_data,
                "user": self.user_data,
                "extra_data": self.extra_data_data,
                "genders": self.gender_data,
            },
            format="json",
        )

        renter_token = self.client.post(self.login, self.user_diff_login, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + renter_token.data["token"]
        )

        response = self.client.post(
            f"/api/borrowed/{book_response.data['id']}/book/",
            {"shipping_method": "Retirada", "finish_date": "2023-01-01"},
            format="json",
        )
        response_feed = self.client.post(
            f"/api/feedback/{response.data['id']}/borrowed/",
            {"stars_renter": 5, "rating_renter": "Very Good"},
            format="json",
        )

        mock_usererror_create = {
            "username": "user_error",
            "password": "senhaforte",
            "birth": "2000-08-12",
            "email": "user@user.com",
        }
        mock_usererror_login = {
            "username": "user_error",
            "password": "senhaforte",
        }
        user_error = User.objects.create_user(**mock_usererror_create)
        user_error_token = self.client.post(
            self.login, mock_usererror_login, format="json"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + user_error_token.data["token"]
        )
        response_feed_error = self.client.post(
            f"/api/feedback/{response.data['id']}/borrowed/",
            {"stars_owner": 5, "rating_Owner": "Very Bad"},
            format="json",
        )
        self.assertTrue(response_feed_error.status_code, 401)
        self.assertEqual(
            response_feed_error.data["message"],
            "you can only post the feedback if you are the owner or renter of the book",
        )
