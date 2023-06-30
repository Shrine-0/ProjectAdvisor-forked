# Creating table for Income
from users.models import myUser
from django.db import models
from Income_Category.models import IncomeCategory


# === Income Model ===

class Income(models.Model):
    user = models.ForeignKey(myUser, related_name="incomes", on_delete=models.SET_NULL, null=True)
    created_Date = models.DateField(auto_now=True)
    incCategory = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0, blank=True)
    note = models.TextField(null=True, blank=True)
    
    
    def __str__(self) -> str:
        return self.user
    
    @staticmethod
    def get_income_total(from_date, to_date, user):
        if from_date == to_date:
            filtered_income =  Income.objects.filter(user=user).filter(date=to_date)
            income_sum = round((sum(income.amount for income in filtered_income)), 2)
            return income_sum
        else:
            filtered_income = (
                Income.objects.filter(user=user)
                .filter(created_Date__range=(from_date, to_date))
                .order_by("-id")
            )
            income_sum = round((sum(income.amount for income in filtered_income)), 2)
            return income_sum

