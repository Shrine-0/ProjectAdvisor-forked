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



from datetime import date, timedelta





## ## Retrives a custom date's expenses on each Category

from datetime import datetime

class QueryCategoryCustomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            start_date_str = request.GET.get('start_date')
            end_date_str = request.GET.get('end_date')
            
            # Convert start_date and end_date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            categories = ExpensesCategory.objects.filter(user=request.user).filter(
                date__range=[start_date, end_date]
            )
            
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Date":category.date,"exCategory": category.name, "amount": total_amount})
            
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        
        except ExpensesCategory.DoesNotExist:
            return Response(
                data={"message": "No categories found for the specified date range."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError:
            return Response(
                data={"message": "Invalid date format. Please provide the date in 'YYYY-MM-DD' format."},
                status=status.HTTP_400_BAD_REQUEST,
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
            start_date = current_date - timedelta(days=current_date.weekday())  # Get the start date of the week
            end_date = start_date + timedelta(days=6)  # Get the end date of the week
            
            print("Start date", start_date)
            print("End date", end_date)
            
            categories = ExpensesCategory.objects.filter(user=request.user).filter(
                date__range=[start_date, end_date]
            )
            
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date__range=[start_date, end_date]
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Date":category.date,"exCategory": category.name, "amount": total_amount})
            
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

## Retrives Today's expenses on each category
class QueryCategoryDayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_date = date.today()  # Get the current date
            
            categories = ExpensesCategory.objects.filter(user=request.user).filter(
                date=current_date
            )
            
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date=current_date
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Date":category.date, "exCategory": category.name, "amount": total_amount})
            
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


## THis View allows you to retrive your expenses on each category in a month
class QueryCategoryMonthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:

            categories = ExpensesCategory.objects.filter(user=request.user).filter(
                date__month=str(current_month)
            )
            
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date__month=current_month
                ).aggregate(total=Sum('amount'))['total']
                data.append({"Date":category.date,"exCategory": category.name, "amount": total_amount})
            
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
            current_year = datetime.now().year
            
            categories = ExpensesCategory.objects.filter(user=request.user).filter(
                date__year=current_year
            )
            
            data = []
            for category in categories:
                total_amount = Expenses.objects.filter(
                    user=request.user,
                    exCategory=category,
                    created_date__year=current_year
                ).aggregate(total=Sum('amount'))['total']
                data.append({"category": category.name, "amount": total_amount})
            
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

        # except:
        #     return Response(
        #         data={"message": "Results not found, Invalid parameters"},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )
        
        except Expenses.DoesNotExist:
            raise NotFound("Expense results not found, Invalid parameters")

        except Income.DoesNotExist:
            raise NotFound("Income results not found, Invalid parameters")

        except Exception as e:
            traceback.print_exc()
            raise NotFound("Error occurred while processing the request")


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