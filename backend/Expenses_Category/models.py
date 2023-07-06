# Creating the Income Category
from users.models import myUser
from django.db import models
from django.dispatch import receiver
from unittest.util import _MAX_LENGTH
from django.utils.html import mark_safe

from django.db.models.signals import post_save



# === Expenses_Category Model ===
class ExpensesCategory(models.Model):
    user = models.ForeignKey(myUser, related_name="expense_categories", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    
    ## Used for showcasing the image in the Admin pannel
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" alt = {self.name} width="50" height="50" />')
    image_tag.short_description = "Image"


@receiver(post_save, sender=myUser)
def create_default_categories(sender, instance, created, **kwargs) -> None:
    if created:
        ExpensesCategory.objects.create(user=instance, name="Food", image = 'media/dish.png')
        ExpensesCategory.objects.create(user=instance, name="Clothing", image = 'media/tshirt.png')
        ExpensesCategory.objects.create(user=instance, name="Transportation", image = 'media/taxi.png')
        ExpensesCategory.objects.create(user=instance, name="Bills", image = 'media/bill.png')
        ExpensesCategory.objects.create(user=instance, name="Education", image = 'media/Education.png')
        ExpensesCategory.objects.create(user=instance, name="Health", image = 'media/health.png')
        ExpensesCategory.objects.create(user=instance, name="Household", image = 'media/home.png')
        ExpensesCategory.objects.create(user=instance, name="Travel", image = 'media/passenger.png')
        ExpensesCategory.objects.create(user=instance, name="Social", image = 'media/social.png')
        ExpensesCategory.objects.create(user=instance, name="Gift", image = 'media/gift.png')
        ExpensesCategory.objects.create(user=instance, name="Others", image = 'media/others.png')
