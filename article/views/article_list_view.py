from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotAuthenticated,
    ParseError,
)
from article.models import Hashtag, Article
from article.serializers import ArticleDetailSerializer, ArticleListSerializer


class ArticlesView(APIView):
    """게시글 리스트 뷰"""

    def get(self, request):
        # 페이징
        try:
            page = request.query_params.get("page", 1)
            # 페이지를 쿼리로 가져온다
            page = int(page)
        except ValueError:
            # 없을시 기본으로 1 페이지로
            page = 1
        page_size = 5
        # 각 페이지 내 게시글갯수
        start = (page - 1) * page_size
        # 페이지 시작 pk
        end = start + page_size
        # 페이지 마지막 게시물 pk
        serializer = ArticleListSerializer(
            Article.objects.all()[start:end],
            # 해당 페이지 게시물들가져오기
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            # 로그인한 유저인지
            serializer = ArticleDetailSerializer(data=request.data)
            if serializer.is_valid():
                # 모델에 유효한 값인지
                article = serializer.save(user=request.user)
                # 작성자가 누구인지 같이 저장한다
                tags = request.data["hashtag"]
                # 사용자가 등록하려고한 태그 스트링 뭉치
                for word in tags.split():
                    if word.startswith("#"):
                        hashtag_obj, created = Hashtag.objects.get_or_create(
                            name=word[1:]
                        )
                        # 각 단어가 해쉬태그엔티티에 존재하면 그 객체를 보내주고 아니면 생성
                        article.hashtag.add(hashtag_obj.pk)
                serializer = ArticleDetailSerializer(article)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated
