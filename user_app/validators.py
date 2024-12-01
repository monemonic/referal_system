import re

from rest_framework import serializers


def validate_phone(obj):
    """
    Проверяет, соответствует ли номер телефона заданному формату
    +* (***) ***-**-**.
    """
    pattern = r'^\+\d{1} \(\d{3}\) \d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, obj):
        raise serializers.ValidationError(
            ('Некорректный формат номера. Номер должен быть формата '
                '+* (***) ***-**-**.')
        )
    return obj
