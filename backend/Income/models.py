# Creating table for Income
from users.models import myUser
from django.db import models
from Income_Category.models import IncomeCategory

from datetime import timedelta, datetime

# imporrting from Core Model
from Core.contstants import today, one_week_ago, current_month
import calendar


# === Income Model ===

class Income(models.Model):
    user = models.ForeignKey(myUser, related_name="incomes", on_delete=models.SET_NULL, null=True)
    created_Date = models.DateField(auto_now=True)
    incCategory = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0, blank=True)
    note = models.TextField(null=True, blank=True)
    
    
    def __str__(self) -> str:
        return str(self.user)
    
    
    ## For gettign the Custom range of Income details
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


    ### PerDay Income Details
    @staticmethod
    def get_income_today(user):
        data = []
        today = datetime.today()
        income_today = Income.objects.filter(user=user, created_Date = today)
        total_amount = sum(income.amount for income in income_today)
        data.append({"date": today.date(), "amount":total_amount})
        return data
    
    
    ## Retrieving last week's Income
    @staticmethod
    def get_income_daily_for_the_week(user):
        data = []
        delta = today - one_week_ago
        for i in range(delta.days + 1):
            day = one_week_ago + timedelta(days=i)
            queryset = Income.objects.filter(user=user).filter(created_Date__startswith=day)
            day_cost = sum([income.amount for income in queryset])
            data.append({"day": day, "amount": day_cost})
        return data
    
    
    
    ### Retriving Income data from a month
    @staticmethod
    def get_income_last_month(user):
        data = []
        today = datetime.today()
        last_month = today.month if today.month > 1 else 12
        last_month_year = today.year if last_month != 12 else today.year - 1
        
        last_month_income = Income.objects.filter(user=user, created_Date__year=last_month_year, created_Date__month=last_month)
        
        total_amount = sum(income.amount for income in last_month_income)
        data.append({"month": calendar.month_name[last_month], "year": last_month_year, "amount": total_amount})
        return data
    
    
    ## Retrieving past 12 Months' data 
    @staticmethod
    def get_income_monthly_for_the_year(user):
        data = []
        for i in range(1, 13):
            months = Income.objects.filter(user=user).filter(created_Date__month=i)
            month_cost = sum([income.amount for income in months])
            month_name = calendar.month_name[i]
            data.append({"month": month_name, "amount": month_cost})
        return data