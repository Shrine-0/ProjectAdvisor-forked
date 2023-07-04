from django.contrib import admin
from .models import ExpensesCategory
# Register your models here.

@admin.register(ExpensesCategory)
class ExpensesCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'image_tag', 'date']
    
    
    # Rename the model name displayed in the admin site
    verbose_name = 'Expense Category'
    verbose_name_plural = 'Expense Categories'
