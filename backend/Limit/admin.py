from django.contrib import admin
from Limit.models import Limit

# Register your models here.
@admin.register(Limit)
class LimitAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "overall_limit", "expenses_Category", "category_limit", "created_date", "updated_date"]
    
    # ===== Adding the way data can be filter ====
    list_filter = ["overall_limit", "category_limit",'created_date', 'expenses_Category', "updated_date"]
    search_fields = ["category_limit", "overall_limit",  "created_date", "updated_date"]

