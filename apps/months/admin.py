from django.contrib import admin

from apps.months.models import Year, Month, PaidMonth


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ("year", )
    ordering = ("-year",)
    search_fields = ("year",)


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ("year", "month")
    list_filter = ("year",)
    ordering = ("-year__year", "month")
    search_fields = ("month",)


@admin.register(PaidMonth)
class PaidMonthAdmin(admin.ModelAdmin):
    list_display = (
        "apartment", "month", "how_much_pay",
        "pay", "is_full_pay", "created_at"
    )
    list_filter = ("is_full_pay", "month__year", "month__month", "apartment__entrance")
    search_fields = ("apartment__apartment_number",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
