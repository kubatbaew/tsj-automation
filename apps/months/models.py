from django.db import models

from apps.apartments.models import Apartment


class Year(models.Model):
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.year)


class Month(models.Model):
    MONTH_CHOICES = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
        5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
        9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }
    year = models.ForeignKey(
        Year, on_delete=models.CASCADE,
        related_name="months_for_year",
    )
    month = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.month)
    
    def get_month_name(self):
        return self.MONTH_CHOICES.get(self.month)


class PaidMonth(models.Model):
    month = models.ForeignKey(
        Month, on_delete=models.SET_NULL,
        null=True, related_name="paids_for_month",
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.SET_NULL,
        null=True, related_name="paid_for_apartment",
    )
    how_much_pay = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
    )
    pay = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
    )
    check_pay = models.FileField(
        upload_to="checks/",
    )
    is_full_pay = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.apartment.apartment_number
