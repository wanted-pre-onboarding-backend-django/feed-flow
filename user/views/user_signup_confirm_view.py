from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from user.models import User
from user.serializers import UserSignupSerializer


class UserSignupConfirmAPIView(generics.GenericAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        account = request.data.get("account")
        auth_code = request.data.get("auth_code")

        print(request.data)

        try:
            user = User.objects.get(account=account)
        except User.DoesNotExist:
            raise ValidationError("없는 계정입니다")
        if user.auth_code != auth_code:
            raise ValidationError("승인번호를 다시 입력 하세요")

        if user.is_approved:
            raise ValidationError("이미 승인된 계정입니다")

        user.is_approved = True
        user.save()

        return Response({"message": "승인이 완료되었습니다"}, status=status.HTTP_200_OK)
