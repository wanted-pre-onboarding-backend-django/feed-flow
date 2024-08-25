from rest_framework.serializers import ModelSerializer
from user.models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["account"]
