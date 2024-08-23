from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "account",
                    "email",
                    "password",
                    "auth_code",
                    "is_activated",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("pk", "account", "email", "is_activated")

    ordering = ()
    filter_horizontal = ()
    list_filter = ()
