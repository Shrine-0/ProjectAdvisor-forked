# Creating table for Income
from users.models import myUser
from django.db import models


# === TodoList Model ===

class TodoList(models.Model):
    
    ## Adding options in the field
    PAYABLE = 'payable'
    RECEIVABLE = 'receivable'
    TYPE_CHOICES = [
        (PAYABLE, 'Payable'),
        (RECEIVABLE, 'Receivable'),
    ]
    
    
    user = models.ForeignKey(myUser, related_name="Todo", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    amount = models.FloatField(default=0, blank=True)
    discription = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return str(self.user)