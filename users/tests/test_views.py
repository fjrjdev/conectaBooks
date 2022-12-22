from django.urls import reverse

from rest_framework.test import APITestCase

from users.models import User

from .mocks import (
    mock_user,
    mock_adm,
    mock_diff,
    mock_user_post,
    mock_adm_login,
    mock_user_login,
    mock_user_diff_login,
)


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.adm_data = mock_adm
        cls.user_data = mock_user_post
        cls.user_wrong_data = mock_user
        cls.user_diff_data = mock_diff

        cls.adm_login = mock_adm_login
        cls.user_login = mock_user_login
        cls.user_diff_login = mock_user_diff_login

        cls.adm = User.objects.create_superuser(**cls.adm_data)
        cls.user_diff = User.objects.create_user(**cls.user_diff_data)

        cls.login = reverse("login")
        cls.base_url = reverse("users")

    def test_can_create_user(self):
        response = self.client.post(self.base_url, self.user_data, format="json")

        data = {
            **response.data,
            "username": self.user_data["username"],
            "email": self.user_data["email"],
            "birth": self.user_data["birth"],
            "address": {
                **response.data["address"],
                "district": self.user_data["address"]["district"],
                "zip_code": self.user_data["address"]["zip_code"],
                "number": self.user_data["address"]["number"],
                "additional_data": self.user_data["address"]["additional_data"],
            },
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)

    def test_cant_create_user_with_same_username(self):
        self.client.post(self.base_url, self.user_data, format="json")
        response = self.client.post(self.base_url, self.user_data, format="json")

        data = {"username": ["A user with that username already exists."]}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, data)

    def test_cant_create_user_with_wrong_keys(self):
        response = self.client.post(
            self.base_url, {**self.user_wrong_data, "address": {}}, format="json"
        )

        data = {
            "district": ["This field is required."],
            "number": ["This field is required."],
            "zip_code": ["This field is required."],
            "city": ["This field is required."],
            "place": ["This field is required."],
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, data)

    def test_can_update_user_with_same_id(self):
        info = {"email": "new@new.com", "birth": "1990-10-10"}

        user = self.client.post(self.base_url, self.user_data, format="json")
        user_token = self.client.post(self.login, self.user_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.patch(
            f"{self.base_url}{user.data['id']}/", info, format="json"
        )

        data = {**response.data, "email": info["email"], "birth": info["birth"]}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

    def test_can_update_user_with_adm_access(self):
        info = {"email": "new@new.com", "birth": "1990-10-10"}

        user = self.client.post(self.base_url, self.user_data, format="json")
        adm_token = self.client.post(self.login, self.adm_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + adm_token.data["token"])

        response = self.client.patch(
            f"{self.base_url}{user.data['id']}/", info, format="json"
        )

        data = {**response.data, "email": info["email"], "birth": info["birth"]}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

    def test_cant_update_user_with_wrong_info(self):
        info = {"email": 1, "birth": 1}

        user = self.client.post(self.base_url, self.user_data, format="json")
        user_token = self.client.post(self.login, self.user_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.patch(
            f"{self.base_url}{user.data['id']}/", info, format="json"
        )

        data = {
            "email": ["Enter a valid email address."],
            "birth": [
                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
            ],
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, data)

    def test_cant_update_user_without_authentication(self):
        info = {"email": "new@new.com", "birth": "1990-10-10"}

        user = self.client.post(self.base_url, self.user_data, format="json")

        response = self.client.patch(
            f"{self.base_url}{user.data['id']}/", info, format="json"
        )

        data = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, data)

    def test_cant_update_user_without_same_id(self):
        info = {"email": "new@new.com", "birth": "1990-10-10"}

        user = self.client.post(self.base_url, self.user_data, format="json")
        user_diff = self.client.post(self.login, self.user_diff_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_diff.data["token"])

        response = self.client.patch(
            f"{self.base_url}{user.data['id']}/", info, format="json"
        )

        data = {"detail": "You do not have permission to perform this action."}

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)

    def test_cant_update_user_with_invalid_user_id(self):
        info = {"email": "new@new.com", "birth": "1990-10-10"}

        user = self.client.post(self.base_url, self.user_data, format="json")
        adm_token = self.client.post(self.login, self.adm_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + adm_token.data["token"])

        response = self.client.patch(f"{self.base_url}1/", info, format="json")

        data = {"detail": "Not found."}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)

    def test_can_delete_user_with_same_id(self):
        user = self.client.post(self.base_url, self.user_data, format="json")
        user_token = self.client.post(self.login, self.user_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.patch(
            f"{self.base_url}{user.data['id']}/soft", None, format="json"
        )

        self.assertEqual(response.status_code, 204)

    def test_can_delete_user_with_adm_access(self):
        user = self.client.post(self.base_url, self.user_data, format="json")
        adm_token = self.client.post(self.login, self.adm_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + adm_token.data["token"])

        response = self.client.patch(
            f"{self.base_url}{user.data['id']}/soft", None, format="json"
        )

        self.assertEqual(response.status_code, 204)

    def test_cant_delete_user_with_wrong_info(self):
        user = self.client.post(self.base_url, self.user_data, format="json")
        user_diff = self.client.post(self.login, self.user_diff_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_diff.data["token"])

        response = self.client.patch(
            f"{self.base_url}{user.data['id']}/soft", None, format="json"
        )

        data = {"detail": "You do not have permission to perform this action."}

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)

    def test_cant_delete_user_with_invalid_id(self):
        user = self.client.post(self.base_url, self.user_data, format="json")
        adm_token = self.client.post(self.login, self.adm_login, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + adm_token.data["token"])

        response = self.client.patch(f"{self.base_url}1/soft", None, format="json")

        data = {"detail": "Not found."}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)
