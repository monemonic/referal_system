from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.crypto import get_random_string

from .constants import (
    LENGTH_CONFIRMATION_CODE,
    LENGTH_INVITE_CODE,
    PHONE_NUMBER_MAX_LENGTH,
    PHONE_NUMBER_MIN_LENGTH,
)
from .validators import validate_phone


class User(AbstractBaseUser):
    """Кастомная модель пользователя"""

    password = None
    phone = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        verbose_name="Номер телефона",
        unique=True,
        validators=[
            validate_phone, MinLengthValidator(PHONE_NUMBER_MIN_LENGTH)
        ],
        help_text="Номер телефона пользователя, формата +* (***) ***-**-**",
    )
    invite_code = models.CharField(
        max_length=LENGTH_INVITE_CODE,
        blank=True,
        null=True,
        validators=[MinLengthValidator(LENGTH_INVITE_CODE)],
        help_text="Личный инвайт-код пользователи.",
    )
    confirmation_code = models.CharField(
        max_length=LENGTH_CONFIRMATION_CODE,
        blank=True,
        null=True,
        validators=[MinLengthValidator(LENGTH_CONFIRMATION_CODE)],
        help_text="Одноразовый код для получения токена.",
    )
    inputed_invite_code = models.CharField(
        max_length=LENGTH_INVITE_CODE,
        blank=True,
        null=True,
        validators=[MinLengthValidator(LENGTH_INVITE_CODE)],
        help_text="Инвайт код введенный пользователем.",
    )
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.pk and not self.invite_code:
            self.invite_code = User.create_invite_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Пользователь {self.phone}"

    @staticmethod
    def create_invite_code():
        invite_code = get_random_string(length=LENGTH_INVITE_CODE)
        if not User.objects.filter(invite_code=invite_code).exists():
            return invite_code
        else:
            User.create_invite_code()


class Invite(models.Model):
    """
    Модель которая сохраняет пару значений пользователя,
    который ввел инвайт код и хозяина инвайт кода
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="invited",
    )
    invite_code_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Хозяин инвайт кода",
        related_name="owner_code",
    )

    class Meta:
        verbose_name = "Инвайт"
        verbose_name_plural = "Инвайты"

    def __str__(self):
        return f"{self.user} {self.invite_code_owner}"
