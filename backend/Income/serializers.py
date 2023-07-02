from rest_framework import serializers
from .models import Income


# === Creating IncomeSerializer Class
class IncomeSerializer(serializers.ModelSerializer):
    
    # Joining name column of ExpensesCategory with Expenses
    incCategory_name = serializers.CharField(source='incCategory.name', read_only=True)
    
    class Meta:
        model = Income
        fields = ["id", "user", "incCategory","incCategory_name", "created_Date", "amount", "note"]