# Generated by Django 4.2.2 on 2023-07-08 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Limit', '0004_remove_limit_category_limits_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='limit',
            name='currency',
        ),
        migrations.AlterField(
            model_name='limit',
            name='created_date',
            field=models.DateField(),
        ),
    ]
