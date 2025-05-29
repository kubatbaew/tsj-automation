from django.contrib import admin

from apps.apartments.models import Entrance, Apartment


@admin.register(Entrance)
class EntranceAdmin(admin.ModelAdmin):
    list_display = ("entrance_number", )
    search_fields = ("entrance_number",)
    ordering = ("entrance_number",)


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("apartment_number", "entrance")
    list_filter = ("entrance",)
    search_fields = ("apartment_number",)
    ordering = ("entrance", "apartment_number")
