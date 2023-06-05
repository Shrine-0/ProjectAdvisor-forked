# Creating the Income Category

from users.models import myUser
from django.db import models
from django.dispatch import receiver


# === Income_Category Model ===
class IncomeCategory(models.Model):
    user = models.ForeignKey(myUser, related_name="categories", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
