from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from article.models import Article
from article.serializers import ArticleStatisticsSerializer, StatisticsDateSerializer


class StatisticsAPIView(APIView):
    """
    Article 통계 정보 조회 API

    이 API는 특정 해시태그와 기간에 따른 게시물 통계를 조회합니다.
    클라이언트는 해시태그, 조회 유형(type), 기간(start, end), 통계 값(value)을 지정할 수 있습니다.
    """
    serializer_class = ArticleStatisticsSerializer

    @swagger_auto_schema(
        operation_summary="Article 통계 정보 조회 API",
        query_serializer=serializer_class,
        responses={
            status.HTTP_200_OK: StatisticsDateSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        GET : /articles/statistics/

        - Parameters:
            - hashtag (string, optional): 조회할 해시태그. 없으면 계정명 사용.
            - type (string, required): 'date' 또는 'hour' 단위 조회.
            - start (date, optional): 조회 시작 날짜. 기본값 7일 전.
            - end (date, optional): 조회 종료 날짜. 기본값 오늘.
            - value (string, optional): 통계 유형. 'count'(기본값), 'view_count', 'like_count', 'share_count'.

        클라이언트가 제공한 쿼리 파라미터를 기반으로 통계 정보를 조회하고 반환합니다.
        """
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid():
            try:
                hashtag = serializer.validated_data['hashtag']
                value = serializer.validated_data['value']
                aggregation_type = serializer.validated_data['type']
                start_date = serializer.validated_data['start']
                end_date = serializer.validated_data['end']

                queryset = self.get_filtered_queryset(start_date, end_date, hashtag)

                statistics = self.get_statistics(queryset, value, aggregation_type)
                serializer = StatisticsDateSerializer(statistics, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                print("An error occurred:", str(e))
                return Response({"detail": "An error occurred while processing your request."}, status=500)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_filtered_queryset(self, start_date, end_date, hashtag):
        """
        주어진 날짜 범위와 해시태그에 따라 필터링된 게시물의 QuerySet을 반환합니다.
        """
        q = Q(created_at__range=(start_date, end_date)) & Q(hashtag__name=hashtag)
        filtered_queryset = Article.objects.prefetch_related("hashtag").filter(q)

        return filtered_queryset

    def get_statistics(self, queryset, value, aggregation_type):
        """
        주어진 queryset에 대해 시계열 통계 정보를 조회하고 반환합니다.

        Args:
            queryset: 데이터베이스에서 조회된 QuerySet입니다.
            value: count, view_count, share_count, like_count 중 하나로, 조회할 값의 유형입니다.
            aggregation_type: 날짜 또는 시간 단위로 데이터를 그룹화하기 위한 함수입니다 (예: TruncDay, TruncHour).

        Returns:
            List of dictionaries:
                - datetime: 집계된 날짜 또는 시간입니다.
                - count: 해당 datetime에서의 집계 결과입니다.

        Raises:
            ValueError: 지원하지 않는 value 값이 전달된 경우 발생합니다.
        """

        # aggregation_type을 사용하여 'created_at' 필드를 날짜 또는 시간 단위로 그룹화하고, 이를 'datetime' 필드로 추가합니다.
        annotated_queryset = (
            queryset
            .annotate(datetime=aggregation_type("created_at"))
            .values("datetime")
        )

        # value에 따른 집계 방법 선택: count인 경우 개수, view_count/like_count/share_count인 경우 합계를 계산
        if value == "count":
            statistics = annotated_queryset.annotate(count=Count("id"))
        elif value in ["view_count", "like_count", "share_count"]:
            statistics = annotated_queryset.annotate(count=Sum(value))
        else:
            raise ValueError(f"Unsupported value: {value}")

        return statistics
