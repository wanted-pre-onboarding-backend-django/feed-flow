from django.urls import path
from rest_framework.routers import DefaultRouter

from article.views import ArticleLikeAPIView

app_name = "article"
router = DefaultRouter()

urlpatterns = [
    path(
        "articles/<int:article_id>/like/",
        ArticleLikeAPIView.as_view(),
        name="article-like",
    )
]

urlpatterns += router.urls
