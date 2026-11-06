import json
import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="gradstudent", password="A-strong-test-password-42")

    def test_dashboard_requires_login_and_displays_username(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "gradstudent")
        self.assertContains(response, "Grad School Party")

    def test_signup_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newgrad",
                "password1": "Another-strong-test-password-42",
                "password2": "Another-strong-test-password-42",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.get(username="newgrad").check_password("Another-strong-test-password-42"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="newgrad").pk)

    def test_login_and_logout_use_django_auth(self):
        response = self.client.post(
            reverse("login"),
            {"username": "gradstudent", "password": "A-strong-test-password-42"},
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)

        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        self.assertRedirects(
            self.client.get(reverse("dashboard")),
            f"{reverse('login')}?next={reverse('dashboard')}",
        )

    def test_user_record_persists_in_database(self):
        persisted_user = User.objects.get(username="gradstudent")
        self.assertEqual(persisted_user.pk, self.user.pk)
        self.assertTrue(persisted_user.check_password("A-strong-test-password-42"))


class CreateFakeGradersCommandTests(TestCase):
    def test_command_is_repeatable_and_does_not_replace_existing_passwords(self):
        accounts = [
            {"username": "grader-one", "password": "grader-one-test-password"},
            {"username": "grader-two", "password": "grader-two-test-password"},
        ]
        output = StringIO()
        with patch.dict(os.environ, {"GRADER_ACCOUNTS_JSON": json.dumps(accounts)}):
            call_command("create_fake_graders", stdout=output)
            existing_user = User.objects.get(username="grader-one")
            existing_user.set_password("user-chosen-password")
            existing_user.save()
            call_command("create_fake_graders", stdout=StringIO())

        self.assertEqual(User.objects.filter(username__startswith="grader-").count(), 2)
        self.assertTrue(User.objects.get(username="grader-one").check_password("user-chosen-password"))
        self.assertTrue(User.objects.get(username="grader-two").check_password("grader-two-test-password"))
        self.assertNotIn("grader-one-test-password", output.getvalue())
