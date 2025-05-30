from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.template.response import TemplateResponse

from apps.months.models import Year, Month, PaidMonth


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ("year",)
    ordering = ("-year",)


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ("year", "month", "report_link")
    list_filter = ("year",)
    ordering = ("-year__year", "month")
    search_fields = ("month",)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:month_id>/report/',
                self.admin_site.admin_view(self.monthly_report_view),
                name='monthly_report',
            ),
        ]
        return custom_urls + urls

    def report_link(self, obj):
        url = reverse("admin:monthly_report", args=[obj.pk])
        return format_html('<a class="button" href="{}">Отчёт</a>', url)
    
    report_link.short_description = "Отчёт"
    report_link.allow_tags = True

    def monthly_report_view(self, request, month_id):
        month = Month.objects.select_related("year").get(pk=month_id)
        payments = PaidMonth.objects.filter(month=month).select_related("apartment")

        total_due = sum(p.how_much_pay for p in payments)
        total_paid = sum(p.pay for p in payments)

        context = dict(
            self.admin_site.each_context(request),
            title=f"Отчёт за {month.get_month_name()} {month.year.year}",
            month=month,
            payments=payments,
            total_due=total_due,
            total_paid=total_paid,
        )

        return TemplateResponse(request, "admin/monthly_report.html", context)



@admin.register(PaidMonth)
class PaidMonthAdmin(admin.ModelAdmin):
    list_display = (
        "apartment", "month", "how_much_pay",
        "pay", "is_full_pay", "created_at"
    )
    list_filter = ("is_full_pay", "month__year", "month__month", "apartment__entrance", "apartment")
    search_fields = ("apartment__apartment_number",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
