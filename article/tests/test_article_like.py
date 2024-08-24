from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from article.models import Article


class ArticleLikeAPITestCase(APITestCase):
    """TestCase for ArticleLikeAPI"""

    def setUp(self):
        # 커스텀 User 모델 가져오기
        User = get_user_model()

        # 테스트 유저 생성
        self.user = User.objects.create_user(
            username="testuser",
            password="test1234!",
            email="testuser@example.com",
        )

        # 로그인
        self.client.login(
            username="testuser",
            password="test1234!",
        )

        # 테스트용 게시글 생성
        self.article = Article.objects.create(
            type="facebook",
            content_id="12345",
            title="Test Article",
            content="This is a test article",
            user=self.user,
        )

        # url 패턴 생성
        self.url = reverse(
            "article:article-like", kwargs={"article_id": self.article.id}
        )

    def test_like_article_success(self):
        """Success like article"""
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # like_cnt 값 1 증가했는지 추가 검증
        self.article.refresh_from_db()
        self.assertEqual(self.article.like_cnt, 1)

    # 외부 API 연동 시 테스트
    # def test_like_article_no_site(self):
    #     """Missing article site"""
    #     # article type 변경
    #     self.article.type = "naver"
    #     self.article.save()

    #     response = self.client.patch(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_article_not_authenticated(self):
        """Request by not authenticated user"""
        self.client.logout()
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_article_invalid_id(self):
        """No matching article are found in the corresponding article_id"""
        url = reverse("article:article-like", kwargs={"article_id": 9999})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_article_generic_error(self):
        """Errors not applicable in the above case"""
        with self.assertRaises(Exception):
            response = self.client.patch(self.url)
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
