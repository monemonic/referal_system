from rest_framework import serializers
from user_app.models import User, Invite
from django.shortcuts import get_object_or_404

from user_app.validators import validate_phone


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя."""

    phone = serializers.CharField(
        validators=[validate_phone], help_text="Номер телефона"
    )

    class Meta:
        fields = ("phone",)
        model = User


class UserReadSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра профиля пользователя."""

    invited_users = UserSerializer(
        read_only=True,
        many=True,
        help_text=(
            "Список всех пользователей, которые "
            "воспользовались инвайт-кодом текущего пользователя"
        ),
    )

    class Meta:
        fields = (
            "phone", "invite_code", "inputed_invite_code", "invited_users"
        )
        model = User

    def to_representation(self, instance):
        # Получения списка всех пользователей,
        # которые воспользовались инвайт-кодом текущего пользователя
        invites = Invite.objects.filter(
            invite_code_owner=instance.id
        ).select_related("user")

        user_objects = [invite.user for invite in invites]
        instance.invited_users = user_objects
        return super().to_representation(instance)


class TokenSerializer(serializers.Serializer):
    """Создание токена для указанного пользователя."""

    phone = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ("phone", "confirmation_code")

    def validate(self, data):
        user = get_object_or_404(User, phone=data["phone"])
        data["user"] = user
        if user.confirmation_code == data["confirmation_code"]:
            return data
        raise serializers.ValidationError("Неверный код")


class InviteCodeSerializer(serializers.ModelSerializer):
    """Ввод инвайт-кода юзером."""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    invite_code_owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        fields = ("user", "invite_code_owner")
        model = Invite

    def validate(self, obj):
        if Invite.objects.filter(user=obj["user"]).exists():
            raise serializers.ValidationError("Вы уже вводили инвайт-код")
        if obj["user"] == obj["invite_code_owner"]:
            raise serializers.ValidationError(
                "Нельзя вводить собственный инвайт-код"
            )
        return obj
