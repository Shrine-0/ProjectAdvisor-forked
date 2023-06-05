from rest_framework import serializers
from .models import Income


# === Creating IncomeSerializer Class
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "user", "incCategory", "created_Date", "amount", "note"]