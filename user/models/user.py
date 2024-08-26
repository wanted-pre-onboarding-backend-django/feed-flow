from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from config.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, account, email, password):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            account=account,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, account, email, password):
        user = self.create_user(
            account=account,
            email=email,
            password=password,
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """User Model Definition"""

    USERNAME_FIELD = "account"
    REQUIRED_FIELDS = ["email"]

    account = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="계정(아이디)",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="이메일",
    )
    password = models.CharField(
        max_length=255,
        null=False,
        verbose_name="비밀번호",
    )
    auth_code = models.CharField(
        max_length=6,
        verbose_name="인증코드",
    )
    is_active = models.BooleanField(
        default=True,
        # 인증코드 승인하는 api 에서 비밀번호과 계정 맞고 그 유저의 인증코드가 일치할때를 찾아야하는데
        # 초기에 false를 해두면 비밀번호계정이 옳아도 그 유저를 반환하지않아 그유저의 인증코트 확인이어렵다
        # 따라서 is_approved를 추가하였다
        verbose_name="활성화 여부",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="관리자 여부",
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="슈퍼유저 여부",
    )
    is_approved = models.BooleanField(default=False)  # 가입 승인을 위한 필드

    objects = CustomUserManager()

    class Meta:
        """Meta definition for User."""

        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    def __str__(self) -> str:
        return f"[{self.id}] {self.account}"
