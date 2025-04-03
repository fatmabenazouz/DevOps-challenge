from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile


class UserProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_profile_creation(self):
        """Test that a profile is created automatically when a user is created"""
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(self.profile.user, self.user)

    def test_profile_str_representation(self):
        """Test the string representation of the UserProfile model"""
        expected_str = f"{self.user.username}'s Profile"
        self.assertEqual(str(self.profile), expected_str)


class RegistrationViewTests(TestCase):
    def test_registration_view_get(self):
        """Test that the registration page loads properly"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_registration_view_post_valid(self):
        """Test user registration with valid data"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "Complex_password123",
                "password2": "Complex_password123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(
            UserProfile.objects.filter(user__username="newuser").exists()
        )

    def test_registration_view_post_invalid(self):
        """Test user registration with invalid data"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "short",
                "password2": "short",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_login_view_get(self):
        """Test that the login page loads properly"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_view_post_valid(self):
        """Test login with valid credentials"""
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_login_view_post_invalid(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpass"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)