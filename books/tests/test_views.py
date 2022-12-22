from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import User
from users.tests.mocks import (
    mock_user,
    mock_diff,
    mock_user_login,
    mock_user_diff_login,
)
from .mocks import mock_book, mock_extra_data, mock_genders


class BookViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = mock_user
        cls.user_diff_data = mock_diff

        cls.book_data = mock_book
        cls.extra_data_data = mock_extra_data
        cls.gender_data = mock_genders

        cls.user = User.objects.create_user(**cls.user_data)
        cls.user_login = mock_user_login

        cls.user_diff = User.objects.create_user(**cls.user_diff_data)
        cls.user_diff_login = mock_user_diff_login

        cls.base_url_user = reverse("users")
        cls.login = reverse("login")
        cls.base_url = reverse("book")

    def test_can_create_book(self):
        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.post(
            self.base_url,
            {
                **self.book_data,
                "user": self.user_data,
                "extra_data": self.extra_data_data,
                "genders": self.gender_data,
            },
            format="json",
        )
        data = {
            **response.data,
            **self.book_data,
            "price": "20.00",
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)

    def test_cant_create_book_with_wrong_keys(self):
        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.post(
            self.base_url,
            {
                "title": "Don Quixote",
            },
            format="json",
        )

        data = {
            "author": ["This field is required."],
            "year": ["This field is required."],
            "price": ["This field is required."],
            "publishing": ["This field is required."],
            "condition": ["This field is required."],
            "isbn": ["This field is required."],
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, data)

    def test_cant_create_book_without_authentication(self):
        response = self.client.post(
            self.base_url,
            {
                **self.book_data,
                # "extra_data": self.extra_data_data,
                "user": self.user_data,
            },
            format="json",
        )

        data = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, data)

    def test_can_get_books(self):
        response = self.client.get(self.base_url, format="json")
        self.assertEqual(response.status_code, 200)

    def test_can_get_book_by_id(self):
        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        book = self.client.post(
            self.base_url,
            {
                **self.book_data,
                "user": self.user_data,
                "extra_data": self.extra_data_data,
                "genders": self.gender_data,
            },
            format="json",
        )

        response = self.client.get(f"/api/book/{book.data['id']}/", format="json")

        self.assertEqual(response.status_code, 200)

    def test_cant_get_book_without_authentication(self):
        response = self.client.get(
            f"/api/book/1/",
            format="json",
        )

        data = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, data)

    def test_cant_get_book_with_wrong_id(self):
        owner_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + owner_token.data["token"])

        book = self.client.post(
            self.base_url,
            {
                **self.book_data,
                "user": self.user_data,
                # "extra_data": self.extra_data_data,
                "genders": self.gender_data,
            },
            format="json",
        )

        user_token = self.client.post(self.login, self.user_diff_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.get(f"/api/book/{book.data['id']}/", format="json")

        data = {"detail": "You do not have permission to perform this action."}

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)

    def test_cant_get_book_with_wrong_id(self):
        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.get(f"/api/book/1/", format="json")

        data = {"detail": "Not found."}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_can_patch_book(self):
        book_patch = {
            "title": "Don Quixote Update",
            "available": False,
            "author": "Miguek de Cervantes Saavedra Update",
        }

        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        book = self.client.post(
            self.base_url,
            {
                **self.book_data,
                "user": self.user_data,
                "extra_data": self.extra_data_data,
                "genders": self.gender_data,
            },
            format="json",
        )
        response = self.client.patch(
            f"/api/book/{book.data['id']}/", book_patch, format="json"
        )

        data = {
            **response.data,
            "title": book_patch["title"],
            "available": book_patch["available"],
            "author": book_patch["author"],
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

    def test_cant_patch_book_without_being_owner(self):
        book_patch = {
            "title": "Don Quixote Update",
            "available": False,
            "author": "Miguek de Cervantes Saavedra Update",
        }

        owner_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + owner_token.data["token"])

        book = self.client.post(
            self.base_url,
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

        response = self.client.patch(
            f"/api/book/{book.data['id']}/", book_patch, format="json"
        )

        data = {"detail": "You do not have permission to perform this action."}

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)

    def test_can_soft_delete_book(self):
        book_delete = {
            "is_active": False
        }

        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        book = self.client.post(
            self.base_url,
            {
                **self.book_data,
                "user": self.user_data,
                "extra_data": self.extra_data_data,
                "genders": self.gender_data,
            },
            format="json",
        )
        response = self.client.patch(
            f"/api/book/{book.data['id']}/soft", book_delete,format="json"
        )

        self.assertEqual(response.status_code, 204)
        
    def test_cant_soft_delete_book(self):
        book_delete = {
            "is_active": False
        }

        owner_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + owner_token.data["token"])

        book = self.client.post(
            self.base_url,
            {
                **self.book_data,
                "user": self.user_data,
                "extra_data": self.extra_data_data,
                "genders": self.gender_data,
            },
            format="json",
        )
        
        diff_token = self.client.post(self.login, self.user_diff_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + diff_token.data["token"])

        response = self.client.patch(
            f"/api/book/{book.data['id']}/soft", book_delete,format="json"
        )

        data = {"detail": "You do not have permission to perform this action."}
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)