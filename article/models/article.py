from django.db import models
from config.models import BaseModel
from user.models import User
from .hashtag import Hashtag


class Article(BaseModel):
    """Article Model Definition"""

    class TypeChoices(models.TextChoices):
        INSTAGRAM = ("instagram", "INSTAGRAM")
        FACEBOOK = ("facebook", "FACEBOOK")
        TWITTER = ("twitter", "TWITTER")
        THREADS = ("threads", "THREADS")

    type = models.CharField(
        max_length=125, choices=TypeChoices.choices, verbose_name="출처 사이트"
    )
    content_id = models.CharField(max_length=255, verbose_name="사이트 내에서의 id(pk)")
    content = models.TextField(default="", verbose_name="게시글 내용")
    view_cnt = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like_cnt = models.PositiveIntegerField(default=0, verbose_name="좋아요 수")
    share_cnt = models.PositiveIntegerField(default=0, verbose_name="공유 횟수")

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자_id")
    hashtag = models.ManyToManyField(Hashtag, verbose_name="해시태그_id")

    class Meta:
        """Meta definition for Article."""

        verbose_name = "Article"
        verbose_name_plural = "Articles"
        db_table = "article"

    def __str__(self) -> str:
        return f"[{self.id}] {self.user.account}"
