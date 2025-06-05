from pathlib import Path
import pdfplumber
import pytesseract
import cv2

import re


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def check_data(text, expected_sum="750", expected_name="Айгул А."):

    return {
        "sum_ok": expected_sum in text,
        "name_ok": expected_name.lower() in text.lower()
    }

def extract_from_image(img_path):
    img = cv2.imread(img_path)
    text = pytesseract.image_to_string(img, lang="rus")
    return text



def extract_sum_and_name(text):
    sum_patterns = [
        r'Итого\s+(\d+[.,]\d{2})',
        r'Сумма\s+(\d+[.,]\d{2})',
        r'(\d+[.,]\d{2})'
    ]

    sum_value = None
    for pattern in sum_patterns:
        match = re.search(pattern, text)
        if match:
            sum_value = match.group(1)
            break

    # Поиск имени после номера и слеша
    name_match = re.search(r'\d{9,}/\s*([А-ЯЁа-яё]+(?:\s[А-ЯЁа-яё]\.))', text)
    name_value = name_match.group(1) if name_match else None

    return sum_value, name_value


# Пример использования
if __name__ == "__main__":
    pdf_file = r"C:\Users\kirad\Desktop\DIPLOM_AUTO_TCG\Backend\check.pdf"
    image_file = r"C:\Users\kirad\Desktop\DIPLOM_AUTO_TCG\Backend\check_img.jpeg"

    if Path(pdf_file).exists():
        pdf_text = extract_from_pdf(pdf_file)
        
        result_pdf = check_data(pdf_text)
        print("PDF Results:", result_pdf)

    if Path(image_file).exists():
        image_text = extract_from_image(image_file)
        result_img = check_data(image_text)
        print("Image Results:", result_img)

    # print("PDF----------------")
    # print(pdf_text)
    # print("IMAGE----------------")
    # print(image_text)

    pdf_sum, pdf_name = extract_sum_and_name(pdf_text)
    img_sum, img_name = extract_sum_and_name(image_text)

    print("PDF sum:", pdf_sum, "name:", pdf_name)
    print("Image sum:", img_sum, "name:", img_name)
