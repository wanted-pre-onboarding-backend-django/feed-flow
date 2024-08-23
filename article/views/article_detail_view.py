from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from article.models import Hashtag, Article
from article.serializers import ArticleDetailSerializer


class ArticleDetailView(APIView):
    """게시물 상세 뷰"""

    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
