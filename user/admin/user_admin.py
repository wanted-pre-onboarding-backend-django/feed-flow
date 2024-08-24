from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin View for User"""

    list_display = (
        "account",
        "email",
        "auth_code",
        "is_active",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "account",
        "email",
    )
    ordering = (
        "created_at",
        "updated_at",
    )
