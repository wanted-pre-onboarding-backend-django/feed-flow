from django.db import models
from ...config.models import BaseModel


# Create your models here.
class Article(BaseModel):
    """Article Model Definition"""

    class TypeChoices(models.TextChoices):
        INSTAGRAM = ("instagram", "INSTAGRAM")
        FACEBOOK = ("facebook", "FACEBOOK")
        TWITTER = ("twitter", "TWITTER")
        THREADS = ("threads", "THREADS")

    type = models.CharField(
        max_length=125,
        choices=TypeChoices.choices,
    )
    content_id = models.CharField(
        max_length=255,
    )
    content = models.TextField(
        default="",
    )
    view_cnt = models.PositiveIntegerField(
        default=0,
    )
    like_cnt = models.PositiveIntegerField(
        default=0,
    )
    share_cnt = models.PositiveIntegerField(
        default=0,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    hashtag = models.ManyToManyField(
        "rooms.Amenity",
    )

    def __str__(self) -> str:
        return self.name
