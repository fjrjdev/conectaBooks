from django.test import TestCase
from pictures.models import Picture


class PicturesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.picture_data = {
            "picture": "testphoto.png",
        }

        cls.picturesTest = Picture.objects.create(**cls.picture_data)

    def test_camp_can_be_null_or_blank(self):

        nullable_picture = self.picturesTest._meta.get_field("picture").null
        blankable_picture = self.picturesTest._meta.get_field("picture").blank
        nullable_book = self.picturesTest._meta.get_field("book").null
        blankable_book = self.picturesTest._meta.get_field("book").blank

        self.assertTrue(nullable_picture)
        self.assertTrue(blankable_picture)
        self.assertTrue(nullable_book)
        self.assertTrue(blankable_book)

    def test_picture_fields(self):
        self.assertEqual(self.picturesTest.picture, self.picture_data["picture"])
        self.assertIsNone(self.picturesTest.book)
