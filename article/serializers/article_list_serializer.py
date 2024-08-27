from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from article.models import Article, Hashtag
from user.serializers import TinyUserSerializer


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["name"]


class ArticleListSerializer(ModelSerializer):
    """게시물 목록 시리얼라이저"""

    user = TinyUserSerializer(read_only=True)
    hashtag = HashtagSerializer(many=True, read_only=True)

    # 유저와 해쉬태그는 이름만
    class Meta:
        model = Article
        fields = [
            "id",
            "type",
            "content_id",
            "title",
            "content",
            "view_cnt",
            "view_cnt",
            "share_cnt",
            "user",
            "hashtag",
            "created_at",
            "updated_at",
        ]

    # 게시물 목록 API에선 content 는 최대 20자 까지만 포함됩니다.
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["content"] = instance.content[:20] + (
            "..." if len(instance.content) > 20 else ""
        )
        return representation
