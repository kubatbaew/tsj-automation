from django.db import models

from django.contrib.auth.models import AbstractUser

from apps.apartments.models import Apartment


class User(AbstractUser):
    apartment = models.OneToOneField(
        Apartment, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="apartment_users_for",
        verbose_name="Квартира"
    )
    father_name = models.CharField(
        max_length=120,
        null=True, blank=True,
        verbose_name="Отчество"
    )
    phone_number = models.CharField(
        max_length=9,
        null=True, blank=True,
        verbose_name="Номер телефона",
    )
    

    def get_phone_number_for_template(self):
        return [self.phone_number[:3], self.phone_number[3:6], self.phone_number[6:9]]

    def __str__(self):
        return super().__str__()
