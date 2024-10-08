from django.urls import path
from rest_framework.routers import DefaultRouter

from article.views import (
    ArticleLikeAPIView,
    ArticleShareAPIView,
    ArticlesView,
    ArticleDetailView,
)
from article.views.article_statistics_api_view import StatisticsAPIView

app_name = "article"
router = DefaultRouter()

urlpatterns = [
    path(
        "",
        ArticlesView.as_view(),
        name="article-list",
    ),
    path(
        "<int:pk>",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path(
        "<int:article_id>/like/",
        ArticleLikeAPIView.as_view(),
        name="article-like",
    ),
    path(
        "<int:article_id>/share/",
        ArticleShareAPIView.as_view(),
        name="article-share",
    ),
    path(
        "statistics",
        StatisticsAPIView.as_view(),
        name="statistics",
    ),
]

urlpatterns += router.urls
