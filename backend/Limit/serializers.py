from rest_framework import serializers
from Limit.models import Limit
from Expenses_Category.models import ExpensesCategory

class LimitSerializer(serializers.ModelSerializer):
    
    # Joining name column of ExpensesCategory with Expenses
    exCategory_name = serializers.CharField(source='expenses_Category.name', read_only=True)

    class Meta:
        model = Limit
        fields = ["id", "user", "overall_limit", "expenses_Category", "exCategory_name", "category_limit", "created_date", "updated_date"]
