# Generated by Django 5.1.3 on 2024-12-01 18:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, help_text='Одноразовый код для получения токена.', max_length=4, null=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='inputed_invite_code',
            field=models.CharField(blank=True, help_text='Инвайт код введенный пользователем.', max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='invite_code',
            field=models.CharField(blank=True, help_text='Личный инвайт-код пользователи.', max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]
