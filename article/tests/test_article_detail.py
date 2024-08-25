from rest_framework.test import APITestCase
from article.models import Article
from user.models import User


class ArticleDetailAPITestCase(APITestCase):
    TITLE = "Original Title"
    CONTENT = "Original Content"
    TYPE = "facebook"
    CONT_ID = "randomId"

    NEW_TITLE = "Updated Title"
    NEW_CONTENT = "Updated Content"
    NEW_TYPE = "twitter"
    NEW_CONT_ID = "newRandomId"

    ACC = "testuser"
    EMAIL = "test@email.com"
    PWD = "test1234!"

    ACC2 = "test2user"
    EMAIL2 = "test2@email.com"
    PWD2 = "test21234!"

    URL = "/articles/"

    def setUp(self):
        User.objects.create_user(
            account=self.ACC,
            email=self.EMAIL,
            password=self.PWD,
        )

        user_2 = User.objects.create_user(
            account=self.ACC2,
            email=self.EMAIL2,
            password=self.PWD2,
        )

        # user2가 쓴 게시물
        self.article = Article.objects.create(
            title=self.TITLE,
            content=self.CONTENT,
            type=self.TYPE,
            content_id=self.CONT_ID,
            user=user_2,
        )

    def test_article_not_found(self):
        response = self.client.get(self.URL + "2")
        self.assertEqual(response.status_code, 404)

    def test_get_article(self):

        response = self.client.get(f"{self.URL}{self.article.id}")

        self.assertEqual(response.status_code, 200)

    def test_put_article_401(self):
        # 로그인 안했을때

        response = self.client.put(
            f"{self.URL}{self.article.id}",
            data={
                "title": self.NEW_TITLE,
                "content": self.NEW_CONTENT,
                "type": self.NEW_TYPE,
                "content_id": self.NEW_CONT_ID,
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_put_article_403(self):
        # 유저1로그인
        self.client.login(account=self.ACC, password=self.PWD)

        # 유저1이 유저2가작성한 게시글수정 시도
        response = self.client.put(
            f"{self.URL}{self.article.id}",
            data={
                "title": self.NEW_TITLE,
                "content": self.NEW_CONTENT,
                "type": self.NEW_TYPE,
                "content_id": self.NEW_CONT_ID,
            },
        )

        # Assert that the response status is 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_put_article_success(self):
        # 유저2로 로그인
        self.client.login(account=self.ACC2, password=self.PWD2)

        # 유저2가 유저2가작성한 게시글수정 시도
        response = self.client.put(
            f"{self.URL}{self.article.id}",
            data={
                "title": self.NEW_TITLE,
                "content": self.NEW_CONTENT,
                "type": self.NEW_TYPE,
                "content_id": self.NEW_CONT_ID,
            },
        )
        self.assertEqual(response.status_code, 200, "200이 아니다")
        self.assertEqual(response.data["title"], self.NEW_TITLE)
        self.assertEqual(response.data["content"], self.NEW_CONTENT)
        self.assertEqual(response.data["type"], self.NEW_TYPE)
        self.assertEqual(response.data["content_id"], self.NEW_CONT_ID)

    def test_put_bad_article(self):
        self.client.login(account=self.ACC2, password=self.PWD2)
        # 유저2가 유저2가작성한 게시글수정 시도
        response = self.client.put(
            f"{self.URL}{self.article.id}",
            data={
                "title": "",
                "content": "",
                "type": "",
                "content_id": "",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "게시글 생성에 옳지않은 글생성",
        )

    def test_del_article_not_login(self):
        response = self.client.delete(f"{self.URL}{self.article.id}")
        self.assertEqual(response.status_code, 401)

    def test_del_article(self):
        self.client.login(account=self.ACC, password=self.PWD)

        # 유저1이 유저2가작성한 게시글삭제 시도
        response = self.client.delete(f"{self.URL}{self.article.id}")
        self.assertEqual(response.status_code, 403)

    def test_del_article_success(self):
        # 유저2로 로그인
        self.client.login(account=self.ACC2, password=self.PWD2)

        # 유저2가 유저2가작성한 게시글삭제 시도
        response = self.client.delete(f"{self.URL}{self.article.id}")
        self.assertEqual(response.status_code, 204)
