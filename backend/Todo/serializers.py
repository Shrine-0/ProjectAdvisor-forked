from rest_framework import serializers
from .models import TodoList


# === Creating IncomeSerializer Class
class TodoListSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = TodoList
        fields = '__all__'