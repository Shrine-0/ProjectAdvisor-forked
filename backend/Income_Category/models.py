# Creating the Income Category

from users.models import myUser
from django.db import models
from django.dispatch import receiver
from django.utils.html import mark_safe

from django.db.models.signals import post_save




# === Income_Category Model ===
class IncomeCategory(models.Model):
    user = models.ForeignKey(myUser, related_name="categories", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    date = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" alt = {self.name} width="50" height="50" />')
    image_tag.short_description = "Image"


@receiver(post_save, sender=myUser)
def create_default_categories(sender, instance, created, **kwargs) -> None:
    if created:
        IncomeCategory.objects.create(user=instance, name="Allowance", image = 'media/allowance.png')
        IncomeCategory.objects.create(user=instance, name="Salary", image = 'media/salary.png')
        IncomeCategory.objects.create(user=instance, name="Others", image = 'media/others.png')
