from django.urls import path
from .views import ExpensesCategoryListView, ExpensesCategoryDetailView

urlpatterns = [
    path("excategory/", ExpensesCategoryListView.as_view(), name="category_list"),
    path("excategory/<int:pk>/", ExpensesCategoryDetailView.as_view(), name="category_detail"),
]
