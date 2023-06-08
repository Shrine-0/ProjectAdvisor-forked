from rest_framework import serializers
from Expenses.models import Expenses

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ["id", "user", "name", "note", "amount", "created_date", "exCategory"]