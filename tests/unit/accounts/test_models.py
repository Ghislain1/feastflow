from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='strongpassword123'
        )

    def test_user_creation(self):
        """Check if a user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('strongpassword123'))

    def test_user_str_return(self):
        """Ensure the __str__ method returns email or expected value"""
        self.assertEqual(str(self.user), self.user.email)

    def test_user_email_unique(self):
        """Check that creating a user with the same email raises an error if unique"""
        User.objects.create_user(username='another', email='unique@example.com', password='pass123')
        with self.assertRaises(ValidationError):
            user_duplicate = User(username='duplicate', email='unique@example.com')
            user_duplicate.full_clean()  # triggers validation

    def test_superuser_creation(self):
        """Ensure superuser has proper flags"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
