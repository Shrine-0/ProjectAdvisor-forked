import datetime
from Expenses_Category.models import ExpensesCategory
from Expenses.models import Expenses
from Expenses.serializers import ExpenseSerializer
from Income_Category.models import IncomeCategory
from Income.models import Income
from Income.serializers import IncomeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Expenses_Category.serializers import CategoryExpenseSerializer

from Core.contstants import INCOME, EXPENSES, current_month, one_month_ago
from Core.helpers import get_trunc_week

import traceback
from rest_framework.exceptions import NotFound


from django.db.models import Sum


from calendar import monthrange, month_name
from datetime import date, timedelta, datetime






### === FOr Income Category ===
## Retrives Today's Income on each category
class QueryIncomeCategoryDayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_date = date.today()  # Get the current date
            income_ids = Income.objects.filter(user=request.user, created_Date=current_date).values_list('incCategory', flat=True)
            
            categories = IncomeCategory.objects.filter(user=request.user, id__in=income_ids)
            data = []
            for category in categories:
                total_amount = Income.objects.filter(
                    user=request.user,
                    incCategory=category,
                    created_Date=current_date
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Date": current_date, "incCategory": category.name, "amount": total_amount})
            
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        
        except IncomeCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the current date."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by Income categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )

## Retrives Weekly Income on each category
class QueryIncomeCategoryWeekView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_date = date.today()  # Get the current date
            start_date = current_date - timedelta(days=current_date.weekday())  # Calculate the start of the current week
            end_date = start_date + timedelta(days=6)  # Calculate the end of the current week

            income_ids = Income.objects.filter(user=request.user, created_Date__range=[start_date, end_date]).values_list('incCategory', flat=True)

            categories = IncomeCategory.objects.filter(user=request.user, id__in=income_ids)
            data = []
            for category in categories:
                total_amount = Income.objects.filter(
                    user=request.user,
                    incCategory=category,
                    created_Date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Start Date": start_date, "End Date": end_date, "incCategory": category.name, "amount": total_amount})

            return Response({"filtered": data}, status=status.HTTP_200_OK)

        except IncomeCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the current week."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by Income categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )


## Retrives Monthly Income on each category
class QueryIncomeCategoryMonthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_date = date.today()  # Get the current date
            start_date = date(current_date.year, current_date.month, 1)  # Calculate the start of the current month
            end_date = date(current_date.year, current_date.month, monthrange(current_date.year, current_date.month)[1])  # Calculate the end of the current month

            income_ids = Income.objects.filter(user=request.user, created_Date__range=[start_date, end_date]).values_list('incCategory', flat=True)

            categories = IncomeCategory.objects.filter(user=request.user, id__in=income_ids)
            data = []
            for category in categories:
                total_amount = Income.objects.filter(
                    user=request.user,
                    incCategory=category,
                    created_Date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Month": month_name[current_date.month], "Start Date": start_date, "End Date": end_date, "incCategory": category.name, "amount": total_amount})

            return Response({"filtered": data}, status=status.HTTP_200_OK)

        except IncomeCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the current month."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by Income categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )



## Retrives Yearly Income on each category
class QueryIncomeCategoryYearView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_year = date.today().year  # Get the current year
            start_date = date(current_year, 1, 1)  # Calculate the start of the current year
            end_date = date(current_year, 12, 31)  # Calculate the end of the current year

            income_ids = Income.objects.filter(user=request.user, created_Date__range=[start_date, end_date]).values_list('incCategory', flat=True)

            categories = IncomeCategory.objects.filter(user=request.user, id__in=income_ids)
            data = []
            for category in categories:
                total_amount = Income.objects.filter(
                    user=request.user,
                    incCategory=category,
                    created_Date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Year": current_year, "Start Date": start_date, "End Date": end_date, "incCategory": category.name, "amount": total_amount})

            return Response({"filtered": data}, status=status.HTTP_200_OK)

        except IncomeCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the current year."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by Income categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )



## Retrives Custom Income on each category
class QueryIncomeCategoryCustomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            start_date_str = request.GET.get('start_date')  # Get the start date from the URL query parameters
            end_date_str = request.GET.get('end_date')  # Get the end date from the URL query parameters

            # Parse the start and end dates from the string format to date objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            income_ids = Income.objects.filter(user=request.user, created_Date__range=[start_date, end_date]).values_list('incCategory', flat=True)

            categories = IncomeCategory.objects.filter(user=request.user, id__in=income_ids)
            data = []
            for category in categories:
                total_amount = Income.objects.filter(
                    user=request.user,
                    incCategory=category,
                    created_Date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Start Date": start_date, "End Date": end_date, "incCategory": category.name, "amount": total_amount})

            return Response({"filtered": data}, status=status.HTTP_200_OK)

        except IncomeCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the specified date range."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by Income categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )



### === FOr Expenses Category
## ## Retrives a custom date's expenses on each Category
class QueryCategoryCustomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')

            # Convert the start date and end date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            expenses_ids = Expenses.objects.filter(user=request.user, created_date__range=[start_date, end_date]).values_list('exCategory', flat=True)

            categories = ExpensesCategory.objects.filter(user=request.user, id__in=expenses_ids)
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Start Date": start_date, "End Date": end_date, "exCategory": category.name, "amount": total_amount})

            return Response({"filtered": data}, status=status.HTTP_200_OK)

        except (ExpensesCategory.DoesNotExist, ValueError):
            return Response(
                data={"message": "Invalid date range or no categories found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            return Response(
                data={"message": "Unable to group by categories"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

## Retrives Today's expenses on each category
class QueryCategoryDayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_date = date.today()  # Get the current date
            expenses_ids = Expenses.objects.filter(user=request.user, created_date=current_date).values_list('exCategory', flat=True)
            
            categories = ExpensesCategory.objects.filter(user=request.user, id__in=expenses_ids)
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date=current_date
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Date": current_date, "exCategory": category.name, "amount": total_amount})
            
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        
        except ExpensesCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the current date."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )

## Retrives a week's expenses on each Category
class QueryCategoryWeekView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_date = date.today()  # Get the current date
            start_date = current_date - timedelta(days=current_date.weekday())  # Calculate the start of the current week
            end_date = start_date + timedelta(days=6)  # Calculate the end of the current week

            expenses_ids = Expenses.objects.filter(user=request.user, created_date__range=[start_date, end_date]).values_list('exCategory', flat=True)

            categories = ExpensesCategory.objects.filter(user=request.user, id__in=expenses_ids)
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Start Date": start_date, "End Date": end_date, "exCategory": category.name, "amount": total_amount})

            return Response({"filtered": data}, status=status.HTTP_200_OK)

        except ExpensesCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the current week."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )



## THis View allows you to retrive your expenses on each category in a month
class QueryCategoryMonthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_date = date.today()  # Get the current date
            start_date = date(current_date.year, current_date.month, 1)  # Calculate the start of the current month
            end_date = date(current_date.year, current_date.month, monthrange(current_date.year, current_date.month)[1])  # Calculate the end of the current month

            expenses_ids = Expenses.objects.filter(user=request.user, created_date__range=[start_date, end_date]).values_list('exCategory', flat=True)

            categories = ExpensesCategory.objects.filter(user=request.user, id__in=expenses_ids)
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Month": month_name[current_date.month],"Start Date": start_date, "End Date": end_date, "exCategory": category.name, "amount": total_amount})

            return Response({"filtered": data}, status=status.HTTP_200_OK)

        except ExpensesCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the current month."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )


## Retriving YEarly data in Expenses Category
class QueryCategoryYearView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_year = date.today().year  # Get the current year

            expenses_ids = Expenses.objects.filter(user=request.user, created_date__year=current_year).values_list('exCategory', flat=True)

            categories = ExpensesCategory.objects.filter(user=request.user, id__in=expenses_ids)
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date__year=current_year
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Year": current_year, "exCategory": category.name, "amount": total_amount})

            return Response({"filtered": data}, status=status.HTTP_200_OK)

        except ExpensesCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the current year."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                data={"message": "Unable to group by categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )



### === Get all the Expenses or Income Details ===
# Get all expenses for a date range(from_date and to_date on front end)
class QueryDateRangeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        select = request.GET.get("select")
        
        try:
            if select == "expenses":
                filtered_expense = (
                    Expenses.objects.filter(user=request.user)
                    .filter(created_date__range=(from_date, to_date))
                    .order_by("-id")
                )
                serializer = ExpenseSerializer(filtered_expense, many=True)
                expense_sum = Expenses.get_expense_total(
                    from_date, to_date, request.user
                )
                json_data = {"filtered": serializer.data, "total": expense_sum}
                if json_data:
                    return Response(json_data, status=status.HTTP_200_OK)
        
            if select == "income":
                filtered_income = (
                    Income.objects.filter(user=request.user)
                    .filter(created_Date__range=(from_date, to_date))
                    .order_by("-id")
                )
                serializer = IncomeSerializer(filtered_income, many=True)
                income_sum = Income.get_income_total(from_date, to_date, request.user)
                json_data = {"filtered": serializer.data, "total": income_sum}

                if json_data:
                    return Response(json_data, status=status.HTTP_200_OK)
            
            return Response(
            data={"message": "Invalid select parameter"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
        except Expenses.DoesNotExist:
            raise NotFound("Expense results not found, Invalid parameters")

        except Income.DoesNotExist:
            raise NotFound("Income results not found, Invalid parameters")

        except Exception as e:
            traceback.print_exc()
            raise NotFound("Error occurred while processing the request")


### === Getting all the expenses details ===
## Per Day Expenses
class QueryDayGraph(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = Expenses.get_expenses_today(request.user)
            return Response({"Expenses": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get today's expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )



## Last 7 day Transactions
# last 7 days
class QueryWeekGraph(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(
                {"Expenses": Expenses.get_expenses_daily_for_the_week(request.user)},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                data={"message": "Unable to get daily expenses for the last week"},
                status=status.HTTP_400_BAD_REQUEST,
            )


## Last Months Graph
class QueryMonthGraph(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(
                {"filtered": Expenses.get_expenses_last_month(user=request.user)},
                status=status.HTTP_200_OK,
            )

        except:
            return Response(
                data={"message": "Unable to get expenses for each week of the month"},
                status=status.HTTP_400_BAD_REQUEST,
            )


## Last 12 month's Transcations
class QueryYearGraph(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        try:
            data = Expenses.get_expenses_monthly_for_the_year(request.user)
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message":"Unable to get monthly expenses for the year"},
                status=status.HTTP_400_BAD_REQUEST,
            )




### === Getting all the Income details
### Per DAy Income view
class QueryDayIncomeGraph(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = Income.get_income_today(request.user)
            return Response({"Income": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get today's Income"},
                status=status.HTTP_400_BAD_REQUEST,
            )



## Last 7 day Transactions
# last 7 days
class QueryWeekIncomeGraph(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(
                {"Income": Income.get_income_daily_for_the_week(request.user)},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                data={"message": "Unable to get daily income for the last week"},
                status=status.HTTP_400_BAD_REQUEST,
            )




## Last Months Income Graph
class QueryMonthIncomeGraph(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(
                {"filtered": Income.get_income_last_month(user=request.user)},
                status=status.HTTP_200_OK,
            )

        except:
            return Response(
                data={"message": "Unable to get income for each week of the month"},
                status=status.HTTP_400_BAD_REQUEST,
            )


## Last month's Transcations
class QueryYearIncomeGraph(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        try:
            data = Income.get_income_monthly_for_the_year(request.user)
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message":"Unable to get monthly income for the year"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            



### Getting all the Net Expenses
## PerDay Net Expenses
class QueryDayNetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = Expenses.get_net_expenses_per_day(request.user)

            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get per day net expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )



## Weekly Net Expenses
class QueryWeeklyNetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = Expenses.get_net_expenses_per_week(request.user)

            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get weekly net expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )




## Monthly Net Expenses
class QueryMonthNetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = Expenses.get_net_expenses_for_the_month(request.user)

            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get monthly net expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )


## Yearly Net Expenses
class QueryYearNetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = Expenses.get_net_expenses_per_year(request.user)

            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get Yearly net expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )