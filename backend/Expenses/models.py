from django.db import models
from users.models import myUser
from Income.models import Income
from Expenses_Category.models import ExpensesCategory
from datetime import date, timedelta, datetime

# imporrting from Core Model
from Core.contstants import today, one_week_ago, current_month
import calendar


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
    
    ## For getting Expenses
    @staticmethod
    def get_expense_total(from_date, to_date, user):
        if from_date == to_date:
            filtered_expense = Expenses.objects.filter(user=user).filter(date=to_date)
            expense_sum = round(
                (sum(expense.amount for expense in filtered_expense)), 2
            )
            return expense_sum
        else:
            filtered_expense = (
                Expenses.objects.filter(user=user)
                .filter(created_date__range=(from_date, to_date))
                .order_by("-id")
            )
            expense_sum = round(
                (sum(expense.amount for expense in filtered_expense)), 2
            )
            return expense_sum
        
    
    ### perday Expenses Details
    @staticmethod
    def get_expenses_today(user):
        data = []
        today = datetime.today()
        expenses_today = Expenses.objects.filter(user=user, created_date=today)
        total_amount = sum(expense.amount for expense in expenses_today)
        data.append({"date": today.date(), "amount": total_amount})
        return data
        
    
    ## Retrieving last week's expenses
    @staticmethod
    def get_expenses_daily_for_the_week(user):
        data = []
        delta = today - one_week_ago
        for i in range(delta.days + 1):
            day = one_week_ago + timedelta(days=i)
            queryset = Expenses.objects.filter(user=user).filter(created_date__startswith=day)
            day_cost = sum([expense.amount for expense in queryset])
            data.append({"day": day, "amount": day_cost})
        return data
    
    
    # ## Data from each week
    # def get_weekly_for_month(user):
    #     data = []
    #     for i in range(1,5):
    #         weeks = Expenses.objects.filter(user=user).filter(created_date_week=i)
    #         week_cost = sum([expense.amount for expense in weeks])
    #         data.append({""})    
        
        
    #     return filtered
    
    
    ### Retriving Expenses data from a month
    @staticmethod
    def get_expenses_last_month(user):
        data = []
        today = datetime.today()
        last_month = today.month if today.month > 1 else 12
        last_month_year = today.year if last_month != 12 else today.year - 1
        
        last_month_expenses = Expenses.objects.filter(user=user, created_date__year=last_month_year, created_date__month=last_month)
        
        total_amount = sum(expense.amount for expense in last_month_expenses)
        data.append({"month": calendar.month_name[last_month], "year": last_month_year, "amount": total_amount})
        return data

        
    
    ## Retrieving past 12 Months' data 
    @staticmethod
    def get_expenses_monthly_for_the_year(user):
        data = []
        for i in range(1, 13):
            months = Expenses.objects.filter(user=user).filter(created_date__month=i)
            month_cost = sum([expense.amount for expense in months])
            month_name = calendar.month_name[i]
            data.append({"month": month_name, "amount": month_cost})
        return data
    
    
    
    
    
    
    
    
    ### Per Day Net Expenses
    @staticmethod
    def get_net_expenses_per_day(user):
        today = datetime.today()

        total_expenses = Expenses.objects.filter(user=user, created_date =today)
        expense_sum = round(sum(expense.amount for expense in total_expenses), 2)
        expense_names = [str(expense.name) for expense in total_expenses]  # Convert expense names to strings

        total_income = Income.objects.filter(user=user, created_Date=today)
        income_sum = round(sum(income.amount for income in total_income), 2)
        income_names = [str(income.incCategory) for income in total_income]  # Convert income names to strings

        net_value = round(income_sum - expense_sum, 2)

        data = {
            "date": today.date(),
            "expense": {
                "total": expense_sum,
                "expenses_count": len(total_expenses),
                "expenses_names": expense_names,  # Include expense names in the response
            },
            "income": {
                "total": income_sum,
                "income_count": len(total_income),
                "income_names": income_names,  # Include income names in the response
            },
            "net_total": net_value,
        }

        return data
    
    
    
    
    ## Weekly Net Expenses
    @staticmethod
    def get_net_expenses_per_week(user):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        total_expenses = Expenses.objects.filter(user=user, created_date__range=[start_of_week, end_of_week])
        expense_sum = round(sum(expense.amount for expense in total_expenses), 2)
        expense_names = [str(expense.name) for expense in total_expenses]  # Convert expense names to strings

        total_income = Income.objects.filter(user=user, created_Date__range=[start_of_week, end_of_week])
        income_sum = round(sum(income.amount for income in total_income), 2)
        income_names = [str(income.incCategory) for income in total_income]  # Convert income names to strings

        net_value = round(income_sum - expense_sum, 2)

        data = {
            "start_date": {
                "Start Date": start_of_week.date(),
                
            },
            "end_date": {
                "End Date": end_of_week.date(), 
            },
            "expense": {
                "total": expense_sum,
                "expenses_count": len(total_expenses),
                "expenses_names": expense_names,  # Include expense names in the response
            },
            "income": {
                "total": income_sum,
                "income_count": len(total_income),
                "income_names": income_names,  # Include income names in the response
            },
            "net_total": net_value,
        }

        return data
    
    
    
    ### Monthly Net Expenses
    @staticmethod
    def get_net_expenses_for_the_month(user):
        total_expenses = Expenses.objects.filter(user=user, created_date__month=str(current_month))
        expense_sum = round(sum(expense.amount for expense in total_expenses), 2)
        expense_names = [str(expense.name) for expense in total_expenses]  # Convert expense names to strings

        total_income = Income.objects.filter(user=user, created_Date__month=str(current_month))
        income_sum = round(sum(income.amount for income in total_income), 2)
        income_names = [str(income.incCategory) for income in total_income]  # Convert income names to strings

        net_value = round(income_sum - expense_sum, 2)

        data = {
            "date":{
                "Date": current_month,
                },
            "expense": {
                "total": expense_sum,
                "Expenses count": len(total_expenses),
                "Expenses names": expense_names,  # Include expense names in the response
            },
            "income": {
                "total": income_sum,
                "Income count": len(total_income),
                "Income names": income_names,  # Include income names in the response
            },
            "Net Total": net_value,
        }

        return data
    
    
    @staticmethod
    def get_net_expenses_per_year(user):
        today = date.today()
        start_of_year = date(today.year, 1, 1)
        end_of_year = date(today.year, 12, 31)

        total_expenses = Expenses.objects.filter(user=user, created_date__range=[start_of_year, end_of_year])
        expense_sum = round(sum(expense.amount for expense in total_expenses), 2)
        expense_names = [str(expense.name) for expense in total_expenses]  # Convert expense names to strings

        total_income = Income.objects.filter(user=user, created_Date__range=[start_of_year, end_of_year])
        income_sum = round(sum(income.amount for income in total_income), 2)
        income_names = [str(income.incCategory) for income in total_income]  # Convert income names to strings

        net_value = round(income_sum - expense_sum, 2)

        data = {
            "year": today.year,
            "expense": {
                "total": expense_sum,
                "expenses_count": len(total_expenses),
                "expenses_names": expense_names,  # Include expense names in the response
            },
            "income": {
                "total": income_sum,
                "income_count": len(total_income),
                "income_names": income_names,  # Include income names in the response
            },
            "net_total": net_value,
        }

        return data