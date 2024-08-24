from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "account",
            "email",
            "password",
            "auth_code",
            "is_activated",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "auth_code": {"write_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        """새로운 유저를 생성할 때 비밀번호를 해시하여 저장"""
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  # 비밀번호를 해시하여 설정
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """유저 정보를 업데이트할 때 비밀번호를 해시하여 저장"""
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password is not None:
            instance.set_password(password)  # 비밀번호를 해시하여 설정
        instance.save()
        return instance
