from rest_framework.serializers import ModelSerializer
from user.models import User

from django.contrib.auth.password_validation import validate_password


class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["account", "email", "password", "auth_code"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        # 비밀번호 검증
        validate_password(value)
        return value
