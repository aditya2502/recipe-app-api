from unittest.mock import patch
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@example.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')


    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='test123',
            is_superuser=True
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_recipe(self):
         user = get_user_model().objects.create_user(
             'test@example.com',
             'test@123'
         )
         recipe= models.Recipe.objects.create(
             user=user,
             title='Sample Recipe',
             description='This is a test recipe',
             time_minutes=10,
             price=Decimal('5.99'),
         )

         self.assertEqual(str(recipe), recipe.title)


    def test_create_tag(self):
        user = sample_user()
        tag = models.Tag.objects.create(user=user , name= "Tag1")
        self.assertEqual(str(tag), tag.name)




