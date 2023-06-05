from rest_framework import serializers
from .models import IncomeCategory

class CategoryIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ["id", "user", "name", "date"]
