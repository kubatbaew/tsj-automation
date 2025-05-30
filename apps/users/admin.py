from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "apartment")
    search_fields = ("username", "email", "first_name", "last_name", "father_name")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name", "father_name", "email", "phone_number")}),
        ("Информация о квартире", {"fields": ("apartment",)}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("password1", "password2", "first_name", "last_name", "father_name", "email", "phone_number", "apartment", "is_active", "is_staff", "is_superuser"),
        }),
    )