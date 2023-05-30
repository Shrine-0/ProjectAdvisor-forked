from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# ===== Creating CUSTOM MANAGER =======
class myManager(BaseUserManager):
    def create_user(self, fName, lName,username, date_of_birth, email, tc, phone, password=None, password2=None):
        # Creates and saves a User with the given email, name, tc, and password
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fName=fName,
            username=username,
            date_of_birth=date_of_birth,
            lName=lName,
            phone=phone,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fName, lName,username, date_of_birth, email, tc, phone, password=None, password2=None):

        # Creates and saves a superuser with the given email, admin type, and password.

        user = self.create_user(
            fName=fName,
            lName=lName,
            date_of_birth=date_of_birth,
            email=email,
            username =username,
            tc=tc,
            phone=phone,
            password=password,
            password2=password2,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


# ==== customUser ====
class myUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    tc = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default = False)
    username = models.CharField(max_length=100, default='')
    fName = models.CharField(max_length=100)
    lName = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # creating the object of myManager

    objects = myManager()

    # == making sure user can login from email only ==

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','fName', 'lName', 'tc', 'date_of_birth', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"

        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
