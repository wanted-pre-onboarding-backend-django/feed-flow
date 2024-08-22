from django.db import models
from ...config.models import BaseModel


class Hashtag(BaseModel):
    """Hashtag Model Definiton"""

    name = models.CharField(
        max_length=50, unique=True, null=False, blank=False, verbose_name="해시태그명"
    )

    class Meta:
        """Meta definition for Hashtag."""

        verbose_name = "Hashtag"
        verbose_name_plural = "Hashtags"
        db_table = "hashtag"

    def __str__(self) -> str:
        return self.name
