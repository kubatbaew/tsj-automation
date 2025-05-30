from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.months.models import PaidMonth

from decimal import Decimal


from api.logics import extract_from_pdf, extract_from_image, check_data, extract_sum_and_name

from pathlib import Path
import tempfile
import os
import re

from django.utils.timezone import now

class SimpleUploadView(APIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('chech_pay')  # проверь правильность имени поля
        paid_id = request.POST.get("paid_id")

        if not uploaded_file:
            return Response({'error': 'Файл не найден'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            paid = PaidMonth.objects.get(id=paid_id)
        except PaidMonth.DoesNotExist:
            return Response({'error': 'Запись с таким paid_id не найдена'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Получен файл: {uploaded_file.name}, размер: {uploaded_file.size} байт")

        # Сохраняем файл во временный, закрываем и открываем заново для чтения
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file.flush()
            temp_path = temp_file.name

        try:
            ext = Path(temp_path).suffix.lower().replace('.', '')
            if ext == 'pdf':
                text = extract_from_pdf(temp_path)
            elif ext in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
                text = extract_from_image(temp_path)
            else:
                return Response({'error': 'Неподдерживаемый формат файла'}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем данные
            check_result = check_data(text)

            # Извлекаем сумму и имя
            sum_value, name_value = extract_sum_and_name(text)

        finally:
            # Удаляем временный файл
            if os.path.exists(temp_path):
                os.remove(temp_path)

        # Проверка имени (регистронезависимо)
        if not name_value or name_value.strip().upper() != "АЙГУЛ А.":
            return Response({'error': 'Неправильный чек: неверное имя получателя'}, status=status.HTTP_400_BAD_REQUEST)

        # Преобразуем сумму к числу — для этого уберём пробелы и заменим запятую на точку
        if sum_value:
            sum_clean = sum_value.replace(' ', '').replace(',', '.')
            try:
                sum_float = float(sum_clean)
            except ValueError:
                return Response({'error': 'Неправильный формат суммы'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Сумма не найдена в чеке'}, status=status.HTTP_400_BAD_REQUEST)


        paid.pay = Decimal(str(sum_float))

        # вычитаем сумму оплаты из how_much_pay
        paid.how_much_pay = paid.how_much_pay - paid.pay

        if paid.how_much_pay <= 0:
            paid.is_full_pay = True
            paid.how_much_pay = Decimal('0')

        # сохраняем файл чека
        paid.check_pay = uploaded_file
        paid.created_at = now()

        paid.save()

        return Response({
            'check': check_result,
            'sum': sum_value,
            'name': name_value,
            'raw_text': text[:500]  # первые 500 символов для отладки
        }, status=status.HTTP_200_OK)
