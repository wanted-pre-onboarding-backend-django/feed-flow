from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from user.serializers import TinyUserSerializer
from user.models import User
from rest_framework.exceptions import NotFound


class UserPublicAPIView(APIView):

    def get(self, request, account):
        try:
            user = User.objects.get(account=account)
        except User.DoesNotExist:
            raise NotFound
        serializer = TinyUserSerializer(user)
        return Response(serializer.data)
