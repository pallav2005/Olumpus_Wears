from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import SignUpForm
from .models import Customer


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class LoginViewTests(TestCase):
    def setUp(self):
        self.password = "StrongPass123!"
        self.user = User.objects.create_user(
            username="TestUser",
            email="testuser@example.com",
            password=self.password,
        )

    def test_login_accepts_email_address(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser@example.com", "password": self.password},
            follow=True,
        )

        self.assertRedirects(response, reverse("store"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)
        self.assertTrue(Customer.objects.filter(user=self.user).exists())

    def test_login_matches_username_case_insensitively(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": self.password},
            follow=True,
        )

        self.assertRedirects(response, reverse("store"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_login_ignores_unsafe_next_redirects(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser@example.com",
                "password": self.password,
                "next": "https://malicious.example/phishing",
            },
        )

        self.assertRedirects(response, reverse("store"), fetch_redirect_response=False)


class SignUpFormTests(TestCase):
    def test_signup_form_rejects_duplicate_email(self):
        User.objects.create_user(
            username="existing-user",
            email="existing@example.com",
            password="AnotherStrongPass123!",
        )

        form = SignUpForm(
            data={
                "username": "new-user",
                "email": "Existing@Example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
