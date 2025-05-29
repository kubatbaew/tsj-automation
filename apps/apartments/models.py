from django.db import models


class Entrance(models.Model):
    entrance_number = models.CharField(
        max_length=4,
    )
    
    def __str__(self):
        return self.entrance_number


class Apartment(models.Model):
    entrance = models.ForeignKey(
        Entrance, on_delete=models.CASCADE,
        related_name="entrance_apartments_for",
    )
    apartment_number = models.CharField(
        max_length=4,
    )
    total_area = models.FloatField(
        default=0,
    )

    def get_total_area(self):
        return str(self.total_area).replace(".", ",")

    def __str__(self):
        return self.apartment_number
