from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError
from user.serializers import UserSignupSerializer
from user.models import User
import random
import string


class UserSignupAPIView(APIView):

    def generate_random_string(self):
        characters = (
            string.ascii_letters + string.digits
        )  # 대문자, 소문자, 숫자를 포함한 문자열 집합
        random_string = "".join(random.choice(characters) for _ in range(6))
        return random_string

    def post(self, request):
        # 인증코드 생성
        request.data["auth_code"] = self.generate_random_string()
        account = request.data.get("account")
        email = request.data.get("email")
        password = request.data.get("password")
        if not password or not account or not email:
            raise ParseError
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()

            # 인증코드 발송하는 함수
            # def sendEmailAuthCode(email, auth_code):

            serializer = UserSignupSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
