from rest_framework.test import APITestCase
from article.models import Article
from user.models import User


class ArticleListAPITestCase(APITestCase):

    TITLE = "Title Test"
    CONTENT = "Content Test"
    TYPE = "facebook"
    CONT_ID = "randomId"

    ACC = "testuser"
    EMAIL = "test@email.com"
    PWD = "test1234!"

    URL = "/articles/"

    def setUp(self):
        user = User.objects.create(
            account=self.ACC,
            email=self.EMAIL,
            password=self.PWD,
        )
        user.set_password(self.PWD)
        user.save()
        self.user = user

        Article.objects.create(
            title=self.TITLE,
            content=self.CONTENT,
            type=self.TYPE,
            content_id=self.CONT_ID,
            user=self.user,
        )

    def test_article_list(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "게시글 리스트 못불러옴")
        self.assertIsInstance(data, list, "받은 데이터 종류가 리스트가 아님")

    def test_create_logout_article(self):
        # 로그인 안하고 글생성 시도
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 401)

    def test_create_bad_article(self):
        # 로그인
        self.client.force_login(self.user)

        # 형식에 맞지않는 게시글 생성
        response = self.client.post(
            self.URL,
            data={
                "title": self.TITLE,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "게시글 생성에 옳지않은 글생성",
        )

    def test_create_article(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.URL,
            data={
                "title": self.TITLE,
                "content": self.CONTENT,
                "type": self.TYPE,
                "content_id": self.CONT_ID,
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "게시글 생성 실패",
        )
