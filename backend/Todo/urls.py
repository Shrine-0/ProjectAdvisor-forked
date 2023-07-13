from django.urls import path

from Todo.views import TodoListView, TodoListDetailView, AmountView

app_name = "Todo"

urlpatterns = [
    
    ## === For Performing Basic CRUD Operation ===
    path("todo/", TodoListView.as_view(), name="todo"),
    path("todo/<int:pk>/", TodoListDetailView.as_view(), name="todo_id"),
    
    ## === for fetching total receivable and payable amount ===
    path('amount/', AmountView.as_view(), name='amountView'),

    

]
