from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from article.models import Hashtag, Article
from article.serializers import ArticleDetailSerializer, ArticleListSerializer


class ArticlesView(APIView):

    def get(self, request):
        pass

    def post(self, request):
        pass
