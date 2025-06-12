import os
import pytesseract
import re
from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path

# Set Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    # Normalize to absolute path
    pdf_path = Path(pdf_path).resolve()
    print(f"📄 Converting PDF to images: {pdf_path}")

    images = convert_from_path(str(pdf_path))  # Convert Path object to str

    all_text = ""
    for i, image in enumerate(images):
        print(f"🔍 Running OCR on page {i + 1}")
        text = pytesseract.image_to_string(image)
        all_text += f"\n\n--- PAGE {i + 1} ---\n\n{text}"

    return all_text

# Example usage
#sample_pdf = "uploads/Boston_Boarding_Passes.pdf"
#extracted_text = extract_text_from_pdf(sample_pdf)
#print(extracted_text)

def parse_ocr_text(text):
    """
    Extracts key qualification data from raw OCR output.
    Looks for:
    - Name
    - Rate
    - Weapon
    - Date Qualified
    - Score
    """

    data = {}

    # Extract Name
    name_match = re.search(r'(?:Name|NAME):?\s+([A-Z ,.\'-]+)', text, re.IGNORECASE)
    if name_match:
        data['name'] = name_match.group(1).strip()

    # Extract Rate
    rate_match = re.search(r'(?:Rate|RATE):?\s+([A-Z0-9/]+)', text, re.IGNORECASE)
    if rate_match:
        data['rate'] = rate_match.group(1).strip()

    # Extract Weapon
    weapon_match = re.search(r'(M9|M4/M16|M500)', text)
    if weapon_match:
        data['weapon'] = weapon_match.group(1)

    # Extract Date Qualified
    date_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    if date_match:
        data['date_qualified'] = date_match.group(1)

    # Extract Score
    score_match = re.search(r'(?:Score|TOTAL|TOTAL SCORE):?\s+(\d{2,3})', text, re.IGNORECASE)
    if score_match:
        data['score'] = score_match.group(1)

    print("🧠 Parsed Data:", data)
    return data
