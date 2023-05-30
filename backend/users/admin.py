from django.contrib import admin
from users.models import myUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):

    # == The Fields to be used in displaying the User Model
    list_display = ('id', 'email', 'username',
                    'date_of_birth', 'phone', 'tc', 'is_admin')

    # ===== Adding the way data can be filter ====
    list_filter = ('is_admin', 'email', 'username')

    # === adding a fieldsets ===
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'fName',
         'lName', 'date_of_birth', 'phone', 'tc')}),
        ('permissions', {'fields': ('is_admin', 'is_active')})
    )

    # == Here we write a field that is displayed in a create object page
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'username','tc', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'fName', 'lName', 'phone')
    ordering = ('email', 'id')
    filter_horizontal = ()


# Now registering the new UserModelAdmin
admin.site.register(myUser, UserModelAdmin)
