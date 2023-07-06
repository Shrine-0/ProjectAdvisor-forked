from django.contrib import admin
from .models import IncomeCategory
# Register your models here.

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',"image_tag", 'user', 'date']
