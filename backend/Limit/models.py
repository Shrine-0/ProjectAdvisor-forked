from django.db import models
from users.models import myUser
from Expenses_Category.models import ExpensesCategory


from django.db.models.signals import post_save
from django.dispatch import receiver


# === Expenses Limit Model ===
class Limit(models.Model):
    user = models.ForeignKey(myUser, related_name="Limit", on_delete=models.SET_NULL, null=True)
    # currency = models.CharField(max_length=30, blank=True, null=True, default="Rs.")
    overall_limit = models.FloatField(default=0,blank=True)
    expenses_Category = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE, null=True, blank=True)
    category_limit = models.FloatField(default=0,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.user)


# @receiver(post_save, sender=myUser)
# def create_limit(sender, instance, created, **kwargs):
#     if created:
#         expenses_categories = ExpensesCategory.objects.filter(user=instance)
#         Limit.objects.create(user=instance, overall_limit=0)
#         for category in expenses_categories:
#             Limit.objects.create(user=instance, expenses_Category=category, category_limit=0)
        
