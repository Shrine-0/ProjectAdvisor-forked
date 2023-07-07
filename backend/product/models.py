from users.models import myUser

from django.db import models
from django.contrib.auth.models import User

class Category(models.TextChoices):
    Free = "Free"
    Premium = "Premium" 

class Product(models.Model):
    name  = models.CharField(max_length=200,blank=False,choices = Category.choices,default=Category.Free)
    description = models.CharField(max_length=200,blank = False,default="Try it for Free")
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    user = models.ForeignKey(myUser,on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)        

    def __str__(self):
        id=str(self.id)
        return id