from django.contrib import admin
from Income.models import Income
# Register your models here.

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'incCategory', 'user', 'amount' , 'created_Date', 'note']
