from django.contrib import admin
from Todo.models import TodoList
# Register your models here.

@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'amount' , 'discription', 'type', 'date', 'created_date']
    
     # ===== Adding the way data can be filter ====
    list_filter = ['title', 'type']
    search_fields = ["title", "type", 'date']
