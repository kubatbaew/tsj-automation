import os
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apps.apartments.models import Entrance, Apartment


for i in range(155, 202):
    # print(i)
    Apartment.objects.create(
        entrance=Entrance.objects.all()[3],
        apartment_number=i,
        total_area=round(random.uniform(49, 100), 2),
    )

print("Вы успешно создали квартиры")
