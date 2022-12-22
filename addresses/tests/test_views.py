from django.urls import reverse

from rest_framework.test import APITestCase

from users.tests.mocks import mock_user, mock_diff, mock_user_login
from users.models import User

from addresses.models import Address

from .mocks import mock_address


class AddressViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address_data = mock_address
        cls.user_data = mock_user
        cls.user_diff_data = mock_diff
        cls.user_login = mock_user_login

        cls.user = User.objects.create_user(**cls.user_data)
        cls.address = Address.objects.create(**{**cls.address_data, "user": cls.user})

        cls.user_diff = User.objects.create_user(**cls.user_diff_data)
        cls.address = Address.objects.create(
            **{**cls.address_data, "user": cls.user_diff}
        )

        cls.login = reverse("login")
        cls.base_url = reverse("address", args=[cls.user.id])
        cls.base_url_wrong_user = reverse("address", args=[cls.user_diff.id])
        cls.base_url_not_found = reverse("address", args=["1"])
    
    def test_can_update_address_details(self):
        update_address = {
            "zip_code": "30105022",
            "number": "22A",
            "additional_data": "informações adicionais atualizadas",
        }

        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.patch(self.base_url, update_address, format="json")

        data = {
            **response.data,
            "district": self.address_data["district"],
            **update_address,
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

    def test_cant_update_address_without_authentication(self):
        update_address = {
            "zip_code": "30105022",
            "number": "22A",
            "additional_data": "informações adicionais atualizadas",
        }

        response = self.client.patch(self.base_url, update_address, format="json")

        data = {"detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, data)

    def test_cant_update_address_without_same_id(self):
        update_address = {
            "zip_code": "30105022",
            "number": "22A",
            "additional_data": "informações adicionais atualizadas",
        }

        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.patch(
            self.base_url_wrong_user, update_address, format="json"
        )

        data = {"detail": "You do not have permission to perform this action."}

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)

    def test_cant_update_address_without_correct_id(self):
        update_address = {
            "zip_code": "30105022",
            "number": "22A",
            "additional_data": "informações adicionais atualizadas",
        }

        user_token = self.client.post(self.login, self.user_login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.data["token"])

        response = self.client.patch(
            self.base_url_not_found, update_address, format="json"
        )

        data = {"detail": "Not found."}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, data)
