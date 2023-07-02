from datetime import datetime, time, timedelta

INCOME = "income"
EXPENSES = "expenses"

today = datetime.now().date()
tomorrow = today + timedelta(1)
today_start = datetime.combine(today, time())
today_end = datetime.combine(tomorrow, time())
one_week_ago = today - timedelta(days=7)
one_month_ago = today - timedelta(days=30)
current_month = today.month

# print("Today",today)
# print("Tomorrow",tomorrow)
# print("Start",today_start)
# print("Today ENd",today_end)
# print("Week Ago",one_week_ago)
# print("Month Ago",one_month_ago)
# print("Current_month",current_month)