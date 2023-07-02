from rest_framework import serializers
from Expenses.models import Expenses
from Expenses_Category.models import ExpensesCategory

class ExpenseSerializer(serializers.ModelSerializer):
    
    # Joining name column of ExpensesCategory with Expenses
    exCategory_name = serializers.CharField(source='exCategory.name', read_only=True)

    class Meta:
        model = Expenses
        fields = ["id", "user", "name", "note", "amount", "created_date", "exCategory", "exCategory_name"]
