"""
Serializers for the user API view.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

# Serializer converts json object into python/django objects that
# can also validate input from the user api.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        # Dictate the fields that the user can use.
        fields = ['email', 'password', 'name']
        # Set the password to write only to prevent reading of passwords.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # Overwriting the create method to ensure create_user method used.
        # Ensures that the password is encrypted.
        return get_user_model().objects.create_user(**validated_data)
