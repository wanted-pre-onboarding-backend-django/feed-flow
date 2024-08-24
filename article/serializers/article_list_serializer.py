from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from article.models import Article, Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["name"]


class ArticleListSerializer(ModelSerializer):

    hashtag = HashtagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = "__all__"

    # 필드 커스텀을 위한 함수 to_representation함수(장고함수)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # content 필드를 20자로 제한하여 반환
        representation["content"] = instance.content[:20] + (
            "..." if len(instance.content) > 20 else ""
        )
        return representation
