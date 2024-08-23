from django.db import models
from config.models import BaseModel


class User(BaseModel):
    """User Model Definition"""

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
        max_length=50,
        verbose_name="인증코드",
    )
    is_activated = models.IntegerField(
        default=0,
        verbose_name="활성화 여부",
    )

    class Meta:
        """Meta definition for User."""

        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    def __str__(self) -> str:
        return f"[{self.id}] {self.account} ({self.email})"
