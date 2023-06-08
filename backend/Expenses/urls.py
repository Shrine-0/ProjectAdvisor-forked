from django.urls import path

from Expenses.views import ExpensesListView,ExpensesDetailView

urlpatterns = [
    path("expenses/", ExpensesListView.as_view(), name="expense_list"),
    path("expenses/<int:pk>/", ExpensesDetailView.as_view(), name="expense_detail"),
]
