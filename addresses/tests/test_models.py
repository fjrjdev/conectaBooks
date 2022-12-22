from django.test import TestCase

from uuid import uuid4

from users.models import User
from users.tests.mocks import mock_user

from addresses.models import Address
from .mocks import mock_address


class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = mock_user
        cls.address_data = mock_address

        cls.user = User.objects.create_user(**cls.user_data)
        cls.address = Address.objects.create(**{**cls.address_data, "user": cls.user})

    def test_address_model(self):
        address = Address.objects.get(id=self.address.id)

        id = address._meta.get_field("id")
        state = address._meta.get_field("state")
        city = address._meta.get_field("city")
        district = address._meta.get_field("district")
        place = address._meta.get_field("place")
        number = address._meta.get_field("number")
        zip_code = address._meta.get_field("zip_code")
        additional_data = address._meta.get_field("additional_data")

        self.assertIsInstance(address, Address)
        self.assertEqual(address, self.address)

        self.assertIsNotNone(id)
        self.assertEqual(id.default, uuid4)
        self.assertTrue(id.primary_key)
        self.assertFalse(id.editable)

        self.assertTrue(state.max_length, 100)
        self.assertFalse(state.null)
        self.assertFalse(state.blank)

        self.assertTrue(city.max_length, 100)
        self.assertFalse(city.null)
        self.assertFalse(city.blank)

        self.assertTrue(district.max_length, 100)
        self.assertFalse(district.null)
        self.assertFalse(district.blank)

        self.assertTrue(place.max_length, 100)
        self.assertFalse(place.null)
        self.assertFalse(place.blank)

        self.assertTrue(number.max_length, 100)
        self.assertFalse(number.null)
        self.assertFalse(number.blank)

        self.assertTrue(zip_code.max_length, 8)
        self.assertFalse(zip_code.null)
        self.assertFalse(zip_code.blank)

        self.assertTrue(additional_data.null)
        self.assertTrue(additional_data.blank)

        self.assertIsInstance(address.user, User)
        self.assertTrue(address.user, self.user)
