"""
Test custom Django management commands.
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# --------------------------------------------------------------
# IMPORTANT - patch works from the inside out, i.e. Nested
# patch decorators will the the first parameters.
# --------------------------------------------------------------


# Simulate the response from the custom django command using mock.
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database when database ready."""
        # Mock the return value of the call to wait_for_db
        patched_check.return_value = True

        # Call db attempted but due to mock only returns true
        call_command('wait_for_db')

        # Assert that the command was called just once.
        patched_check.assert_called_once_with(databases=['default'])

    # Replace the sleep method with a majic mock object.
    # Means test won't sleep but rather pass straight away.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when there is an operational error."""
        # Mock 2 psycopg2 errors, 3 operational errors and then return true.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # Ensure the command was called 6 times to account for
        # 5 mock errors then true.
        self.assertEqual(patched_check.call_count, 6)

        patched_check.assert_called_with(databases=['default'])
