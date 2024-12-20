# Generated by Django 5.1.3 on 2024-12-01 11:35

import django.core.validators
import user_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(help_text='Номер телефона пользователя, формата +* (***) ***-**-**', max_length=20, unique=True, validators=[user_app.validators.validate_phone, django.core.validators.MinLengthValidator(18)], verbose_name='Номер телефона'),
        ),
    ]
