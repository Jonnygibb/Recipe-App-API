"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


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
