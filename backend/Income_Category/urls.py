from django.urls import path

from .import views

urlpatterns = [
    path("incomecategory/", views.CategoryListView.as_view(), name="category_list"),
    path("incomecategory/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
]
