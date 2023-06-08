from django.db import models
from users.models import myUser
from Income.models import Income
from Expenses_Category.models import ExpensesCategory
from datetime import timedelta

# === Expenses Model ===
class Expenses(models.Model):
    user = models.ForeignKey(myUser, related_name="expenses", on_delete=models.SET_NULL, null=True )
    name = models.CharField(max_length=30, blank=True, null=True)
    amount = models.FloatField(default=0, blank=True)
    exCategory = models.ForeignKey(
        ExpensesCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    created_date = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name