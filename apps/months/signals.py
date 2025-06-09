from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.months.models import Year, Month, PaidMonth
from apps.apartments.models import Apartment


@receiver(post_save, sender=Year)
def create_months_for_year(sender, instance, created, **kwargs):
    if created:
        for month_number in range(1, 13):
            Month.objects.create(year=instance, month=month_number)


@receiver(post_save, sender=Month)
def create_paid_for_all_apartments(sender, instance, created, **kwargs):
    if created:
        apartments = Apartment.objects.all()
        for apartment in apartments:
            PaidMonth.objects.create(
                month=instance,
                apartment=apartment,
                how_much_pay=750,
            )
