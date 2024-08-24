from datetime import datetime, timedelta
from rest_framework import serializers


class ArticleStatisticsSerializer(serializers.Serializer):
    """
    Serializer definition for ArticleStatisticsSerializer.
    : StatisticsAPIView에서 입력받은 쿼리 파라미터를 검증하기 위해 사용됩니다.
    """
    hashtag = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    type = serializers.ChoiceField(
        choices=["date", "hour"],
        required=True,
    )
    start = serializers.DateField(
        default=lambda: datetime.now().date() - timedelta(days=7),
    )
    end = serializers.DateField(
        default=lambda: datetime.now().date(),
    )
    value = serializers.ChoiceField(
        choices=["count", "view_count", "like_count", "share_count"],
        required=False,
        default="count",


class StatisticsDateSerializer(serializers.Serializer):
    """
    Serializer definition for StatisticsDateSerializer.
    : 날짜와 시간 단위의 통계 데이터를 직렬화하는데 사용됩니다.
    """
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    count = serializers.IntegerField()
