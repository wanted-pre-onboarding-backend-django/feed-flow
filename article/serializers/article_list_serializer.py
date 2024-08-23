from rest_framework.serializers import ModelSerializer
from article.models import Article


class ArticleListSerializer(ModelSerializer):
    """게시물 리스트 시리얼라이저"""

    class Meta:
        model = Article
        fields = (
            "pk",
            "title",
            "type",
            "content_id",
            "like_cnt",
        )
