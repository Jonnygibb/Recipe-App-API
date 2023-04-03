"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successfully(self):
        """Test creating a user with an email successfully."""
        email = 'test@example.com'
        password = 'testpass123'
        # Use django auth system to get custom user model.
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        # Check user is made with email and password specified.
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """Test email is normalised for new users."""
        # Anything before the @ symbol can retain capitalisation
        # however after the email, the domain must be lowercase
        # in the standard implemented here.
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test1@Example.com', 'Test1@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        # Iterate over sample and expected email, create each email
        # a user object and check email is correctly normalised in object.
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_address_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            # Create a user with a blank email.
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful"""
        # Create a user since the recipe will be assigned to a user.
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpassword123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description',
            )
        
        self.assertEqual(str(recipe), recipe.title)

