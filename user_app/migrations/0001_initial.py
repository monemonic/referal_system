# Generated by Django 5.1.3 on 2024-12-01 11:03

import django.core.validators
import django.db.models.deletion
import user_app.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(help_text='Номер телефона пользователя, формата +* (***) ***-**-**', max_length=20, unique=True, validators=[user_app.validators.validate_phone], verbose_name='Номер телефона')),
                ('invite_code', models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6)])),
                ('confirmation_code', models.CharField(blank=True, max_length=4, null=True, validators=[django.core.validators.MinLengthValidator(4)])),
                ('inputed_invite_code', models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_code_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_code', to=settings.AUTH_USER_MODEL, verbose_name='Хозяин инвайт кода')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invited', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Инвайт',
                'verbose_name_plural': 'Инвайты',
            },
        ),
    ]
