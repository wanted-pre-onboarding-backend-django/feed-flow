from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from article.models import Article, Hashtag
from article.serializers import ArticleDetailSerializer
from django.shortcuts import get_object_or_404


class ArticleDetailView(APIView):
    """게시물 상세 뷰"""

    def get_object(self, pk):
        # 게시물 아이디값에 따라 게시물을 찾거나 없으면 404를 보낸다
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        # 게시물 아이디값에 따라 게시물을 찾아 보낸다
        Article = self.get_object(pk)
        # API 호출 시, 해당 게시물 view_count 가 1 증가합니다.
        cookie_name = f"hit_{pk}"
        serializer = ArticleDetailSerializer(Article)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        if cookie_name not in request.COOKIES:
            Article.view_cnt += 1
            Article.save()
            response.set_cookie(cookie_name, "true", max_age=86400)
            # 서버 시갓 24시간 후 만료 쿠키
        return response

    def put(self, request, pk):
        # 게시물의 수정하는 경우
        Article = self.get_object(pk)
        if not request.user.is_authenticated:
            # 유저가 로그인을 하지 않았을시
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if Article.user != request.user:
            # 글쓴이가 아닐시
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleDetailSerializer(
            Article,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            article = serializer.save(user=request.user)
            tags = request.data.get("hashtag", "")
            # 사용자가 등록하려고한 뭉치
            for word in tags.split():
                if word.startswith("#"):
                    hashtag_obj, created = Hashtag.objects.get_or_create(name=word[1:])
                    # 각 단어가 해쉬태그엔티티에 존재하면 그 객체를 보내주고 아니면 생성
                    article.hashtag.add(hashtag_obj.pk)
            serializer = ArticleDetailSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Article = self.get_object(pk)
        if not request.user.is_authenticated:
            # 유저가 로그인 안되어있을시
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if Article.user != request.user:
            # 해당 게시글 글쓴이 아닐시
            return Response(status=status.HTTP_403_FORBIDDEN)
        Article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
