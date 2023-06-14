from django.contrib import admin
from Expenses.models import Expenses

# Register your models here.
@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "note", "amount", "created_date", "exCategory"]
    
    # ===== Adding the way data can be filter ====
    list_filter = ['name', 'created_date', 'exCategory']
    search_fields = ["name", "note", "amount", "created_date"]

