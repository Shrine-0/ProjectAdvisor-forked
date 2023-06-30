from rest_framework import serializers
from .models import ExpensesCategory

class CategoryExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensesCategory
        fields = ["id", "user", "name","image", "date"]