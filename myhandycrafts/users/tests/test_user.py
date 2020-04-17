"""User Test."""

#Django

from django.test import TestCase

# Model
from myhandycrafts.categories.models import Category

class UserMangerTestCase(TestCase):
    """User Manager test case."""

    def setUp(self):
        """ Test Case setup."""
        self.category = Category.objects.create(
            name='Madera',
            description='Artesanías de madera',
        )


    def test_categories(self):
        """Random generate."""
        self.assertEqual(self.category.name,'Madera')
        self.assertEqual(self.category.description,'Artesanías de madera')

    def test_categories2(self):
        """Random generate."""
        self.assertEqual(self.category.name,'Madera')
        self.assertEqual(self.category.description,'Artesanías de madera')





