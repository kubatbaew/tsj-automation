from django.db import models

from apps.apartments.models import Apartment


class Year(models.Model):
    year = models.PositiveSmallIntegerField(
        verbose_name="Год",
        help_text="Введите год (например: 2030)"
    )

    def __str__(self):
        return str(self.year)
    
    class Meta:
        verbose_name = "Год"
        verbose_name_plural = "Года"


class Month(models.Model):
    MONTH_CHOICES = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
        5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
        9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }
    year = models.ForeignKey(
        Year, on_delete=models.CASCADE,
        related_name="months_for_year",
        verbose_name="Год",
        help_text="Выберите год"
    )
    month = models.PositiveSmallIntegerField(
        verbose_name="Месяц",
        help_text="Введите номер месяца (например: 5, 9, 12)"
    )

    def __str__(self):
        return str(self.month)
    
    def get_month_name(self):
        return self.MONTH_CHOICES.get(self.month)
    
    class Meta:
        verbose_name = "Месяц"
        verbose_name_plural = "Месяца"


class PaidMonth(models.Model):
    month = models.ForeignKey(
        Month, on_delete=models.SET_NULL,
        null=True, related_name="paids_for_month",
        verbose_name="Месяц",
        help_text="Выберите Месяц"
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.SET_NULL,
        null=True, related_name="paid_for_apartment",
        verbose_name="Квартира",
        help_text="Выберите квартиру"
    )
    how_much_pay = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name="Сколько нужно оплатить",
    )
    pay = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name="Сколько оплатил",
    )
    check_pay = models.FileField(
        upload_to="checks/",
        verbose_name="Чек",
    )
    is_full_pay = models.BooleanField(
        default=False,
        verbose_name="Статус полной оплаты",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    def __str__(self):
        return self.apartment.apartment_number

    class Meta:
        verbose_name = "Оплата месяца"
        verbose_name_plural = "Оплата месяцов"