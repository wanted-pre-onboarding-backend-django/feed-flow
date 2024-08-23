from django.db import models


class BaseModel(models.Model):
    """Base Model Definiton"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name="추가된 일시",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="수정된 일시",
        auto_now=True,
    )
