from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    """Testing core models."""
    def test_create_user_with_email_successfully(self):
        """Test creating user with email successfully"""
        email = 'test@example.com'
        password = '12345test'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalaized(self):
        """Test normalize emails"""
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@example.com', 'test2@example.com'],
            ['test_3@example.com', 'test_3@example.com'],
            ['test4@EXample.COM', 'test4@example.com'],
        ]
        password = '1a9r86'
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password=password)
            self.assertEqual(user.email, expected)

    def test_new_invalid_email(self):
        """Test invalid emails."""
        with self.assertRaises(ValueError):
            email = ''
            password = '12345test'
            get_user_model().objects.create_user(email=email, password=password)

    def test_create_user_with_staff(self):
        email = 'test@example.com'
        password = '12345test'
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)
