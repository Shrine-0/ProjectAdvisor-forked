from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    #====Simple JWT====
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    
    # === adding urls of User Module ===
    path('api/user/',include('users.urls')),

    # === URLS of Income
    path('income/', include('Income.urls')),
    
    #! == Subscription URLS for Order,Producr,Checkout
    path("product/",include("product.urls")),
    path("order/",include("order.urls")),
    
    # === Adding urls of Income Category
    path('incomeCat/',include('Income_Category.urls')),
    
    # === URLS of Expenses
    path('expenses/', include('Expenses.urls')),

    # === Adding urls of Income Category
    path('expensesCat/',include('Expenses_Category.urls')),
    
    # === Core ====
    path("core/", include("Core.urls", namespace="Core")),
    
    # === Core ====
    path("limit/", include("Limit.urls", namespace="Limit")),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)