"""
Serializers for the user API view.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import gettext as _

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

    def update(self, instance, validated_data):
        """
        Update and return user. Overwrites the update method that is called
        on models when they are updated.
        """
        # Retrieve and remove the password if it exists.
        password = validated_data.pop('password', None)
        # Call the update method on the modelSerializer base class.
        # This way, existing update code is utilsed and only necessary
        # code is overwritten.
        user = super().update(instance, validated_data)

        # If the user sepcified an update to their password..
        if password:
            # set and save the password.
            user.set_password(password)
            user.save()

        # Djangorestframework expects the model to be returned.
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    # Use the email and password in the authentication token
    # serializer.
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        # In case the user has a space at end of password.
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user. This method is called by the view
        to validate the data sent to the API.
        """
        # Get email and pw from user input.
        email = attrs.get('email')
        password = attrs.get('password')
        # Authenticate the user against the user model.
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # If the user was unsuccessfully authenticated,
        # raise and display error.
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            # Validation error will generate HTTP_400_BAD_REQUEST
            raise serializers.ValidationError(msg, code='authorization')

        # Set the user attribute if authentication successful.
        attrs['user'] = user
        return attrs
