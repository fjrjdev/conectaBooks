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

from borroweds.models import Borrowed


class BorrowedViewTest(APITestCase):
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

    def test_can_create_borrowed(self):
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

        book = Book.objects.get(id=book_response.data["id"])
        data = {
            **response.data,
            "user_id": self.user_diff.id,
            "book_id": book.id,
        }

        self.assertTrue(response.status_code, 201)
        self.assertTrue(response.data, data)

    def test_cant_create_borrowed_with_available_false(self):
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

        self.client.post(
            f"/api/borrowed/{book_response.data['id']}/book/",
            {"shipping_method": "Retirada", "finish_date": "2023-01-01"},
            format="json",
        )

        response = self.client.post(
            f"/api/borrowed/{book_response.data['id']}/book/",
            {"shipping_method": "Retirada", "finish_date": "2023-01-01"},
            format="json",
        )

        data = {"detail": "This book is not available."}

        self.assertTrue(response.status_code, 400)
        self.assertTrue(response.data, data)

    def test_cant_owner_create_a_borrowed(self):
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

        response = self.client.post(
            f"/api/borrowed/{book_response.data['id']}/book/",
            {"shipping_method": "Retirada", "finish_date": "2023-01-01"},
            format="json",
        )

        data = {"detail": "You do not have permission to perform this action."}

        self.assertTrue(response.status_code, 403)
        self.assertTrue(response.data, data)

    def test_can_devolution(self):
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

        get_borrewed_book = self.client.post(
            f"/api/borrowed/{book_response.data['id']}/book/",
            {"shipping_method": "Retirada", "finish_date": "2023-01-01"},
            format="json",
        )

        devolution_borrewed_book = self.client.patch(
            f"/api/borrowed/{book_response.data['id']}/devolution/",
            {},
            format="json",
        )

        book = Book.objects.get(id=book_response.data["id"])

        self.assertTrue(book.available)
        self.assertEqual(devolution_borrewed_book.status_code, 200)

    def test_devolution_not_borrowed(self):
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

        devolution_borrewed_book = self.client.patch(
            f"/api/borrowed/{book_response.data['id']}/devolution/",
            {},
            format="json",
        )

        book = Book.objects.get(id=book_response.data["id"])

        self.assertEqual(devolution_borrewed_book.data["detail"], "Books is available")
        self.assertEqual(devolution_borrewed_book.status_code, 400)
