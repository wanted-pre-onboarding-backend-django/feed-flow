from django.contrib.auth import authenticate
from rest_framework.response import Response

# from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt


class UserLogInAPIView(APIView):
    def post(self, request):
        account = request.data.get("account")
        password = request.data.get("password")
        if not account or not password:
            raise ParseError
        user = authenticate(
            account=account,
            password=password,
        )

        if user is not None:

            if not user.is_approved:
                # 사용자가 비활성화된 경우
                raise AuthenticationFailed(
                    "계정이 비활성화되었습니다. 이메일 인증을 확인해주세요."
                )

            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            # response = JsonResponse({"redirect_url": "/articles"}, status=200)

            # response.set_cookie(
            #     key="jwt",
            #     value=token,
            #     httponly=True,  # XSS 공격으로부터 보호하기 위해 JavaScript에서 접근 불가
            #     secure=False,  # HTTPS를 통해서만 쿠키 전송 (생산 환경에서 사용) 실제론 True
            #     samesite="Strict",  # 크로스 사이트 요청 방지
            #     max_age=3600,  # 쿠키의 수명을 1시간으로 설정
            # )

            return Response({"token": token})
        else:
            raise AuthenticationFailed("아이디 또는 비밀번호가 잘못되었습니다.")
