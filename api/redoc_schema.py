from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import (InviteCodeSerializer, TokenSerializer,
                          UserReadSerializer, UserSerializer)

REDOC_SCHEMA = {
    "users_input_invite_code": swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "invite_code": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Инвайт код другого пользователя",
                    example="iyGedV",
                )
            },
        ),
        responses={
            201: InviteCodeSerializer,
            400: openapi.Response(
                description="Указан неверный инвайт-код.",
                examples={
                    "application/json": {
                        "detail": "Указан неверный инвайт-код."
                    }
                },
            ),
            409: openapi.Response(
                description="Вы уже вводили инвайт-код.",
                examples={
                    "application/json":
                    {"detail": "Вы уже вводили инвайт-код."}},
            ),
            422: openapi.Response(
                description="Нельзя вводить собственный инвайт-код",
                examples={
                    "application/json": {
                        "detail": "Нельзя вводить собственный инвайт-код."
                    }
                },
            ),
        },
        operation_description=(
            "Ввод и сохранение инвайт-кода для текущего пользователя."
        ),
    ),
    "code": swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="Успешная отправка кода",
                examples={"application/json": {"detail": "Код отправлен"}},
            ),
            400: openapi.Response(
                description="Некорректный формат номера",
                examples={
                    "application/json": {
                        "phone": (
                            "['Некорректный формат номера."
                            "Номер должен быть формата +* (***) ***-**-**]"
                        )
                    }
                },
            ),
        },
    ),
    "me": swagger_auto_schema(
        responses={
            200: UserReadSerializer,
            401: openapi.Response(
                description="Учетные данные не были предоставлены.",
                examples={
                    "application/json": {
                        "detail": "Учетные данные не были предоставлены."
                    }
                },
            ),
        }
    ),
    "token": swagger_auto_schema(
        request_body=TokenSerializer,
        responses={
            200: openapi.Response(
                description="Токен авторизации",
                examples={"application/json": {
                    "access": "asdkasdjak123k12j31Djdasp"
                }},
            ),
            404: openapi.Response(
                description="Пользователь не найден",
                examples={
                    "application/json": {
                        "detail": "No User matches the given query."
                    }
                },
            ),
            400: openapi.Response(
                description="Неверный код",
                examples={"application/json": {
                    "non_field_errors": "Неверный код"
                }},
            ),
        },
    ),
}
