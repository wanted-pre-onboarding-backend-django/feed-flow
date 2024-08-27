from rest_framework.serializers import ModelSerializer
from article.models import Article, Hashtag
from user.serializers import TinyUserSerializer


class HashtagSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("name",)


class ArticleDetailSerializer(ModelSerializer):
    """게시물 상세 시리얼라이저"""

    user = TinyUserSerializer(read_only=True)
    # 유저정보는 최대한 간단히 보여준다
    hashtag = HashtagSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "type",
            "content_id",
            "user",
            "hashtag",
            "created_at",
            "updated_at",
            "view_cnt",
            "like_cnt",
            "share_cnt",
        ]
