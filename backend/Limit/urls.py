from django.urls import path

from Limit.views import LimitListView, LimitDetailView, OverallLimitView, CompareCategoryView

app_name = "Limit"

urlpatterns = [
    
    ## === For Performing Basic CRUD Operation ===
    path("limit/", LimitListView.as_view(), name="limit"),
    path("limit/<int:pk>/", LimitDetailView.as_view(), name="limit_id"),
    # path("compare/", CompareOverallView.as_view(), name="limit_Overall"),
    
    
    ### === FOr comparing limit with overall Expenses ===
    path("OverallLimitView/", OverallLimitView.as_view(), name="limit_Overall"),
    
    ### === For comparing the limit with each budget ===
    path("categoryLimitView/", CompareCategoryView.as_view(), name="limit_Overall"),
    

]
