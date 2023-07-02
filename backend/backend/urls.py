from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    #====Simple JWT====
    path('api/token', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    
    # === adding urls of User Module ===
    path('api/user/',include('users.urls')),

    # === URLS of Income
    path('income/', include('Income.urls')),
    
    # === Adding urls of Income Category
    path('incomeCat/',include('Income_Category.urls')),
    
    # === URLS of Expenses
    path('expenses/', include('Expenses.urls')),

    # === Adding urls of Income Category
    path('expensesCat/',include('Expenses_Category.urls')),
    
    # === Core ====
    path("core/", include("Core.urls", namespace="core")),

]
