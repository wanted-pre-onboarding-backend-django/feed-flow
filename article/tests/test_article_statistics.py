from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta
from django.utils import timezone

from article.models import Hashtag, Article


class BaseStatisticsAPITestCase(APITestCase):
    def setUp(self):
        self.now = timezone.now()
        # 커스텀 User 모델 가져오기
        User = get_user_model()

        # 테스트 유저 생성
        self.user = User.objects.create_user(
            account="testuser",
            password="test1234!",
            email="testuser@example.com",
        )

        # 테스트 해시태그 생성
        self.hashtag1 = Hashtag.objects.create(name="testuser")
        self.hashtag2 = Hashtag.objects.create(name="testtag1")
        self.hashtag3 = Hashtag.objects.create(name="testtag2")

        # 테스트 Article 데이터 생성
        self.article1 = Article.objects.create(
            type="instagram",
            content_id="12345",
            title="Test Article 1",
            content="This is a test article 1",
            view_cnt=100,
            like_cnt=50,
            share_cnt=10,
            # created_at=self.now - timedelta(days=1),  # 1일 전
            user=self.user,
        )
        self.article1.hashtag.add(self.hashtag1)
        self.article1.created_at = self.now - timedelta(days=1)
        self.article1.save()

        self.article2 = Article.objects.create(
            type="facebook",
            content_id="12346",
            title="Test Article 2",
            content="This is a test article 2",
            view_cnt=200,
            like_cnt=150,
            share_cnt=20,
            # created_at=self.now - timedelta(days=2),  # 2일 전
            user=self.user,
        )
        self.article2.hashtag.add(self.hashtag1, self.hashtag2)
        self.article2.created_at = self.now - timedelta(days=2)
        self.article2.save()

        self.article3 = Article.objects.create(
            type="twitter",
            content_id="12347",
            title="Test Article 3",
            content="This is a test article 3",
            view_cnt=300,
            like_cnt=250,
            share_cnt=30,
            # created_at=self.now - timedelta(days=5),  # 5일 전
            user=self.user,
        )
        self.article3.hashtag.add(self.hashtag2)
        self.article3.created_at = self.now - timedelta(days=5)
        self.article3.save()

        # 통계 API URL 설정
        self.url = reverse("article:statistics")


class StatisticsAPITestCase(BaseStatisticsAPITestCase):
    def test_access_without_authentication(self):
        """인증되지 않은 사용자가 접근할 때 403 Forbidden이 반환되는지 테스트"""
        response = self.client.get(self.url, {"type": "date"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_with_authentication(self):
        """인증된 사용자가 접근할 때 200 OK가 반환되는지 테스트"""
        self.client.force_login(self.user)
        response = self.client.get(self.url, {"type": "date"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_default_parameters(self):
        """기본값으로 통계 조회가 올바르게 수행되는지 테스트"""
        self.client.force_login(self.user)

        # required 파라미터만을 사용하여 GET 요청
        response = self.client.get(self.url, {"type": "date"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 기본값 확인: start는 7일 전, end는 today, type은 'date'
        start_default = self.now.date() - timedelta(days=7)
        end_default = self.now.date()

        # 응답 데이터가 비어있지 않은지 확인
        self.assertTrue(len(response.data) > 0, "응답 데이터가 비어 있습니다.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in response.data:
            self.assertIn("count", item)
            datetime_str = item["datetime"]
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

            datetime_obj_date = datetime_obj.date()
            self.assertGreaterEqual(datetime_obj_date, start_default)
            self.assertLessEqual(datetime_obj_date, end_default)

    def test_statistics_with_specific_hashtag(self):
        """특정 해시태그로 통계 조회가 올바르게 수행되는지 테스트"""
        self.client.force_login(self.user)

        # 특정 해시태그로 조회 요청
        response = self.client.get(self.url, {"type": "date", "hashtag": "testtag1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터가 비어있지 않은지 확인
        self.assertTrue(len(response.data) > 0, "응답 데이터가 비어 있습니다.")

        expected_counts = {
            "2024-08-21": 1,
            "2024-08-24": 1,
        }

        # 응답 데이터에 특정 해시태그와 관련된 게시물의 통계가 포함되어 있는지 확인
        for item in response.data:
            # 응답 데이터의 날짜 부분만 추출
            datetime_str = item["datetime"]
            date_str = datetime_str.split(" ")[0]  # 날짜 부분만 사용

            # 예상된 날짜의 count 값과 비교
            if date_str in expected_counts:
                self.assertEqual(
                    item["count"],
                    expected_counts[date_str],
                    f"{date_str}에 대한 count 값이 예상과 다릅니다.",
                )
            else:
                self.fail(f"예상치 않은 날짜 {date_str}가 응답에 포함되었습니다.")

    def test_statistics_within_date_range(self):
        """특정 날짜 범위로 통계 조회가 올바르게 수행되는지 테스트"""
        self.client.force_login(self.user)

        # 날짜 범위를 설정하여 조회 요청
        start_date = (self.now.date() - timedelta(days=4)).strftime("%Y-%m-%d")
        end_date = self.now.date().strftime("%Y-%m-%d")

        response = self.client.get(
            self.url,
            {
                "type": "date",
                "start": start_date,
                "end": end_date,
                "hashtag": "testtag1",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터가 비어있지 않은지 확인
        self.assertTrue(len(response.data) > 0, "응답 데이터가 비어 있습니다.")

        # 예상되는 count 값
        expected_counts = {
            (self.now.date() - timedelta(days=2)).strftime(
                "%Y-%m-%d"
            ): 1,  # article2가 2일 전
        }

        # 응답 데이터에 특정 날짜 범위 내의 게시물 통계가 포함되어 있는지 확인
        for item in response.data:
            # 응답 데이터의 날짜 부분만 추출
            datetime_str = item["datetime"]
            date_str = datetime_str.split(" ")[0]  # 날짜 부분만 사용

            # 예상된 날짜의 count 값과 비교
            if date_str in expected_counts:
                self.assertEqual(
                    item["count"],
                    expected_counts[date_str],
                    f"{date_str}에 대한 count 값이 예상과 다릅니다.",
                )
            else:
                self.fail(f"예상치 않은 날짜 {date_str}가 응답에 포함되었습니다.")

    def test_statistics_by_date(self):
        """`type`이 'date'일 때 일별 통계 조회가 올바르게 수행되는지 테스트"""
        self.client.force_login(self.user)

        # `type`을 'date'로 설정하여 조회 요청
        response = self.client.get(
            self.url,
            {
                "type": "date",
                "start": (self.now.date() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "end": self.now.date().strftime("%Y-%m-%d"),
                "hashtag": "testtag1",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터가 비어있지 않은지 확인
        self.assertTrue(len(response.data) > 0, "응답 데이터가 비어 있습니다.")

        # 예상되는 count 값
        expected_counts = {
            (self.now.date() - timedelta(days=5)).strftime(
                "%Y-%m-%d"
            ): 1,  # article3가 5일 전
            (self.now.date() - timedelta(days=2)).strftime(
                "%Y-%m-%d"
            ): 1,  # article2가 2일 전
        }

        # 응답 데이터에 일별 통계가 올바르게 포함되어 있는지 확인
        for item in response.data:
            # 응답 데이터의 날짜 부분만 추출
            datetime_str = item["datetime"]
            date_str = datetime_str.split(" ")[0]  # 날짜 부분만 사용

            # 예상된 날짜의 count 값과 비교
            if date_str in expected_counts:
                self.assertEqual(
                    item["count"],
                    expected_counts[date_str],
                    f"{date_str}에 대한 count 값이 예상과 다릅니다.",
                )
            else:
                self.fail(f"예상치 않은 날짜 {date_str}가 응답에 포함되었습니다.")

    def test_statistics_by_hour(self):
        """`type`이 'hour'일 때 시간별 통계 조회가 올바르게 수행되는지 테스트"""
        self.client.force_login(self.user)

        # `type`을 'hour'로 설정하여 조회 요청
        response = self.client.get(
            self.url,
            {
                "type": "hour",
                "start": (self.now - timedelta(days=2)).strftime("%Y-%m-%d"),
                "end": self.now.strftime("%Y-%m-%d"),
                "hashtag": "testtag1",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 예상되는 count 값 (UTC가 아닌 서울 시간대 기준)
        expected_counts = {
            (
                self.article2.created_at.astimezone(timezone.get_current_timezone())
            ).strftime("%Y-%m-%d %H:00"): 1,
        }

        # 응답 데이터에 시간별 통계가 올바르게 포함되어 있는지 확인
        for item in response.data:
            # 응답 데이터의 날짜 및 시간 부분 추출
            datetime_str = item["datetime"]

            # 예상된 시간의 count 값과 비교
            if datetime_str in expected_counts:
                self.assertEqual(
                    item["count"],
                    expected_counts[datetime_str],
                    f"{datetime_str}에 대한 count 값이 예상과 다릅니다.",
                )
            else:
                self.fail(f"예상치 않은 시간 {datetime_str}가 응답에 포함되었습니다.")

    def test_statistics_by_view_count(self):
        """`value`가 'view_count'일 때 통계 조회가 올바르게 수행되는지 테스트"""
        self.client.force_login(self.user)

        # `value`를 'view_count'로 설정하여 조회 요청
        response = self.client.get(
            self.url,
            {
                "type": "date",
                "start": (self.now - timedelta(days=7)).strftime("%Y-%m-%d"),
                "end": self.now.strftime("%Y-%m-%d"),
                "value": "view_count",
                "hashtag": "testtag1",
            },
        )

        # 상태 코드가 500일 경우, 응답 내용 출력
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            print("서버 오류 발생:", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 예상되는 view_count 값
        expected_view_counts = {
            (self.article2.created_at).strftime("%Y-%m-%d"): self.article2.view_cnt,
            (self.article3.created_at).strftime("%Y-%m-%d"): self.article3.view_cnt,
        }

        # 응답 데이터에 통계가 올바르게 포함되어 있는지 확인
        for item in response.data:
            datetime_str = item["datetime"]
            date_str = datetime_str.split(" ")[0]

            if date_str in expected_view_counts:
                self.assertEqual(
                    item["count"],
                    expected_view_counts[date_str],
                    f"{date_str}에 대한 view_count 값이 예상과 다릅니다.",
                )
            else:
                self.fail(f"예상치 않은 날짜 {date_str}가 응답에 포함되었습니다.")

    def test_statistics_by_like_count(self):
        """`value`가 'like_count'일 때 통계 조회가 올바르게 수행되는지 테스트"""
        self.client.force_login(self.user)

        # `value`를 'like_count'로 설정하여 조회 요청
        response = self.client.get(
            self.url,
            {
                "type": "date",
                "start": (self.now - timedelta(days=7)).strftime("%Y-%m-%d"),
                "end": self.now.strftime("%Y-%m-%d"),
                "value": "like_count",
                "hashtag": "testtag1",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 예상되는 like_count 값
        expected_like_counts = {
            (self.article2.created_at).strftime("%Y-%m-%d"): self.article2.like_cnt,
            (self.article3.created_at).strftime("%Y-%m-%d"): self.article3.like_cnt,
        }

        # 응답 데이터에 통계가 올바르게 포함되어 있는지 확인
        for item in response.data:
            datetime_str = item["datetime"]
            date_str = datetime_str.split(" ")[0]

            if date_str in expected_like_counts:
                self.assertEqual(
                    item["count"],
                    expected_like_counts[date_str],
                    f"{date_str}에 대한 like_count 값이 예상과 다릅니다.",
                )
            else:
                self.fail(f"예상치 않은 날짜 {date_str}가 응답에 포함되었습니다.")

    def test_statistics_by_share_count(self):
        """`value`가 'share_count'일 때 통계 조회가 올바르게 수행되는지 테스트"""
        self.client.force_login(self.user)

        # `value`를 'share_count'로 설정하여 조회 요청
        response = self.client.get(
            self.url,
            {
                "type": "date",
                "start": (self.now - timedelta(days=7)).strftime("%Y-%m-%d"),
                "end": self.now.strftime("%Y-%m-%d"),
                "value": "share_count",
                "hashtag": "testtag1",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 예상되는 share_count 값
        expected_share_counts = {
            (self.article2.created_at).strftime("%Y-%m-%d"): self.article2.share_cnt,
            (self.article3.created_at).strftime("%Y-%m-%d"): self.article3.share_cnt,
        }

        # 응답 데이터에 통계가 올바르게 포함되어 있는지 확인
        for item in response.data:
            datetime_str = item["datetime"]
            date_str = datetime_str.split(" ")[0]

            if date_str in expected_share_counts:
                self.assertEqual(
                    item["count"],
                    expected_share_counts[date_str],
                    f"{date_str}에 대한 share_count 값이 예상과 다릅니다.",
                )
            else:
                self.fail(f"예상치 않은 날짜 {date_str}가 응답에 포함되었습니다.")
