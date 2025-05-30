from django.db import models


class Entrance(models.Model):
    entrance_number = models.CharField(
        max_length=4,
        verbose_name="Номер подъезда",
        help_text="Введите номер подъезда"
    )
    
    def __str__(self):
        return self.entrance_number
    
    class Meta:
        verbose_name = "Подъезд"
        verbose_name_plural = "Подъезды"


class Apartment(models.Model):
    entrance = models.ForeignKey(
        Entrance, on_delete=models.CASCADE,
        related_name="entrance_apartments_for",
        verbose_name="Подъезд",
        help_text="Выберите подъезд"
    )
    apartment_number = models.CharField(
        max_length=4,
        verbose_name="Номер квартиры",
        help_text="Введите номер квартиры"
    )
    total_area = models.FloatField(
        default=0,
        verbose_name="Общая площадь квартиры",
        help_text="Введите общую площадь квартиры (пример: 59.69)"
    )

    def get_total_area(self):
        return str(self.total_area).replace(".", ",")

    def __str__(self):
        return self.apartment_number

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
