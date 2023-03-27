from django.db import models

# Create your models here.
class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.IntegerField()
    f_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.EmailField()
    ph_no = models.IntegerField(max_length=10)
    dob = models.DateField()

    # def __str__(self):
    #     return f"{self.phone_number}, {self.email}"
class plan_type(models.Model):
    plan_type_id= models.AutoField(primary_key=True)
    description= models.CharField(max_length=100)
    payment=models.IntegerField(max_length=50)
    date_of_issue= models.DateField()
    date_of_exp = models.DateField()

class premium(models.Model):
    premium_id= models.AutoField(primary_key=True)
    user_id= models.ForeignKey(user,on_delete=models.CASCADE)
    plan_type = models.ForeignKey(plan_type,on_delete=models.CASCADE)
    status = models.BooleanField()

class credit(models.Model):
    credit_id=models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    amount=models.IntegerField(max_length=50)
    date_of_credit=models.DateField()
    date_of_paid=models.DateField()

class category(models.Model):
    category_id=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=100)

class budget(models.Model):
    budget_id=models.AutoField(primary_key=True)
    category_id=models.ForeignKey(category, on_delete=models.CASCADE)
    user_id=models.ForeignKey(user, on_delete=models.CASCADE)
    amount=models.IntegerField(max_length=50)
    date = models.DateField()

class account(models.Model):
    account_id=models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    acc_number=models.IntegerField(max_length=50)
    balance=models.IntegerField(max_length=50)


class transaction_details(models.Model):
    transaction_id= models.AutoField(primary_key=True)
    account_id=models.ForeignKey(account, on_delete=models.CASCADE)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    category_id = models.ForeignKey(category, on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    desc = models.CharField(max_length=100)
    status = models.BooleanField()
    amount = models.IntegerField(max_length=50)
    date = models.DateField()


