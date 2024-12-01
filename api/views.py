import time

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from user_app.models import User

from .redoc_schema import REDOC_SCHEMA
from .serializers import (
    InviteCodeSerializer,
    TokenSerializer,
    UserReadSerializer,
    UserSerializer
)

DEFAULT_CODE = 1111
SIMULATED_DELAY = 2


class UsersViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @REDOC_SCHEMA["token"]
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(AllowAny,),
        serializer_class=TokenSerializer,
    )
    def token(self, request):
        """Получение токена для указанного пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = AccessToken.for_user(user)

        # После использования код удаляется
        user.confirmation_code = None
        user.save()

        return Response({"access": str(token)}, status=status.HTTP_200_OK)

    @REDOC_SCHEMA["code"]
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(AllowAny,),
    )
    def code(self, request):
        """Получение кода авторизации для указанного пользователя"""

        if "phone" not in request.data:
            return Response(
                {"detail": "Поле phone отсутствует"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Если пользователь не найден в базе данных, добавляет его в бд
        if not User.objects.filter(phone=request.data["phone"]).exists():
            self.create(request)

        user = get_object_or_404(User, phone=request.data["phone"])

        # Имитация задержки
        time.sleep(SIMULATED_DELAY)

        # Код должен генерироваться случайно,
        # но так как его некуда отправлять указан статичный
        user.confirmation_code = DEFAULT_CODE
        user.save()
        return Response({"detail": "Код отправлен"}, status=status.HTTP_200_OK)

    @REDOC_SCHEMA["users_input_invite_code"]
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(IsAuthenticated,),
        serializer_class=InviteCodeSerializer,
    )
    def input_invite_code(self, request):
        """Ввод и сохранение инвайт-кода для текущего пользователя."""
        user = request.user

        # Получение хозяина указанного инвайт-кода
        try:
            owner_invite = User.objects.get(
                invite_code=request.data["invite_code"]
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Указан неверный инвайт-код."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data=({"user": user.id, "invite_code_owner": owner_invite.id})
        )
        serializer.is_valid(raise_exception=True)

        # Записываем инвайт-код в таблицу пользователя.
        user.inputed_invite_code = request.data["invite_code"]
        user.save(update_fields=["inputed_invite_code"])

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @REDOC_SCHEMA["me"]
    @action(
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
        methods=["get"],
        serializer_class=UserReadSerializer,
    )
    def me(self, request):
        """Получение страницы профиля текущего пользователя."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
