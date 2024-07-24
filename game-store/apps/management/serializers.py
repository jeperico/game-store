from .models import Games, User, Player, Category, Genre
from rest_framework import serializers, status
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction

class UserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "created_at",
            "updated_at"
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "last_name",
            "first_name",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            password = validated_data.pop("password")
            first_name = validated_data.get("first_name", "")
            last_name = validated_data.get("last_name", "")
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.name = (
                f"{first_name} {last_name}".strip()
            )
            user.save()

            return user


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    old_password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            "old_password",
            "password",
            "password2"
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class WithUserRegisterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop("user")
            user_data["is_active"] = True
            password = user_data.pop("password")

            user = UserRegisterSerializer.create(
                UserRegisterSerializer(),
                validated_data=user_data
            )
            user.set_password(password)
            user.save()
            validated_data["user"] = user

            return super().create(validated_data)


class ProfileTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserReadOnlySerializer(self.user).data

        return data


class PlayerRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(required=True)

    class Meta:
        model = Player
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user_serializer = UserRegisterSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()

            seller = Player.objects.create(user=user, **validated_data)

            return seller
        else:
            raise serializers.ValidationError(user_serializer.errors)


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
