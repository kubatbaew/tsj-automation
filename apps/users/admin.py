from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "father_name")
    search_fields = ("username", "email", "first_name", "last_name", "father_name")
    ordering = ("username",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Apartment Info", {"fields": ("apartment", "father_name", "phone_number")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("apartment", "father_name", "phone_number")}),
    )
