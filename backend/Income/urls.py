from django.urls import path

from Income.views import IncomeListView, IncomeDetailView

urlpatterns = [
    path("income/", IncomeListView.as_view(), name="income_list"),
    path("income/<int:pk>/", IncomeDetailView.as_view(), name="Income_detail"),
]
