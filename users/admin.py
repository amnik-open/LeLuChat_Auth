"""This file specify how does models show on admin panel"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from users.models import LeluUser


class LeluUserAdmin(UserAdmin):
    """LeluUserAdmin class specify LeluUser model in admin panel"""

    fieldsets = (
    (None, {"fields": ("email", "password", "name")}),
    (_("Personal info"), {"fields": ("first_name",
    "last_name")}),
    (
        _("Permissions"),
        {
            "fields": (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            )
        },
    ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "name", "first_name", "last_name", "is_staff")
    search_fields = ("email", "name", "first_name", "last_name")
    ordering = ("email",)

admin.site.register(LeluUser, LeluUserAdmin)
