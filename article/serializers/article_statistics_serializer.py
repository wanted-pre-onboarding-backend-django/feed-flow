from datetime import datetime, timedelta

from django.db.models.functions import TruncDay, TruncHour
from django.utils import timezone

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
    )

    def validate_start(self, value):
        """
        start_date 필드를 유효성 검사하고, 타임존을 적용하여 datetime 객체로 변환합니다.
        또한, start 날짜가 현재 날짜 이전인지 확인합니다.
        """
        if value >= datetime.now().date():
            raise serializers.ValidationError("The start date must be before today.")

        # 날짜를 타임존이 적용된 datetime 객체로 변환
        return timezone.make_aware(datetime.combine(value, datetime.min.time()))

    def validate_end(self, value):
        """
        end_date 필드를 유효성 검사하고, 타임존을 적용하여 datetime 객체로 변환합니다.
        """
        return timezone.make_aware(datetime.combine(value, datetime.max.time()))

    def validate_type(self, value):
        """
        type 필드의 유효성을 검사하고, 해당하는 Trunc 함수를 반환합니다.
        """
        if value == "date":
            return TruncDay
        elif value == "hour":
            return TruncHour
        else:
            raise serializers.ValidationError("Unsupported date_type")

    def validate_value(self, value):
        """
        `value` 필드를 모델 필드와 매핑하도록 변경.
        """
        value_mapping = {
            "view_count": "view_cnt",
            "like_count": "like_cnt",
            "share_count": "share_cnt",
        }
        return value_mapping.get(value, value)

    def validate(self, data):
        """
        해시태그가 입력되지 않은 경우 사용자 계정명을 해시태그로 설정합니다.
        start_date와 end_date의 논리적 일관성을 검사합니다.
        """
        # 사용자의 계정명을 해시태그로 설정
        request = self.context.get("request")
        if not data.get("hashtag") and request and hasattr(request, "user"):
            data["hashtag"] = request.user.account

        # start_date와 end_date의 일관성 검사
        start_date = data.get("start")
        end_date = data.get("end")

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError(
                "The start date must be before the end date."
            )

        return data


class StatisticsDateSerializer(serializers.Serializer):
    """
    Serializer definition for StatisticsDateSerializer.
    : 날짜와 시간 단위의 통계 데이터를 직렬화하는데 사용됩니다.
    """

    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    count = serializers.IntegerField()
