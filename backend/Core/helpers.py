from django.db.models.functions import TruncWeek
from Expenses.models import Expenses
from django.urls import reverse
from rest_framework.test import APITestCase


def get_trunc_week(user):
    filtered = (
        Expenses.objects.all()
        .filter(user=user)
        .annotate(week=TruncWeek("date"))
        .values("week")
        .annotate(total=sum("amount"))
        .order_by("week")
    )
    return filtered


class AuthenticateUser(APITestCase):
    def authenticate_user(self):
        self.client.post(
            reverse("users:register"),
            {
                "first_name": "test",
                "last_name": "user",
                "email": "user@email.com",
                "username": "testuser",
                "password": "password",
            },
        )
        response = self.client.post(
            reverse("users:login"),
            {
                "username": "testuser",
                "password": "password",
            },
        )
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")