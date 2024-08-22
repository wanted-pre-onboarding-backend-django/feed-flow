from django.db import models
from ...config.models import BaseModel


class Hashtag(BaseModel):
    """Hashtag Model Definiton"""

    name = models.CharField(
        max_length=50,
    )

    def __str__(self) -> str:
        return self.name
