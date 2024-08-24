from django.contrib import admin
from article.models import Article, Hashtag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "type",
        "content_id",
        "user",
        "view_cnt",
        "like_cnt",
        "share_cnt",
        "created_at",
    )

    list_filter = (
        "type",
        "user",
        "hashtag",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "=user__account",
    )


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
