from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","email," "password1", "password2"),
            },
        ),
    )