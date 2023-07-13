from django.urls import path

from Todo.views import TodoListView, TodoListDetailView

app_name = "Todo"

urlpatterns = [
    
    ## === For Performing Basic CRUD Operation ===
    path("todo/", TodoListView.as_view(), name="todo"),
    path("todo/<int:pk>/", TodoListDetailView.as_view(), name="todo_id"),
    # path("compare/", CompareOverallView.as_view(), name="limit_Overall"),

    

]
