import re
from datetime import datetime

def parse_ocr_text(text):
    """
    Parses raw OCR text from a scanned 3591/1 form and returns structured data as a dict.
    This is a placeholder using simple regex patterns. Will be expanded.
    """
    data = {}

    # Example parsing logic — these patterns must be adapted to real 3591 layouts
    name_match = re.search(r"Name[:\s]+([A-Z][a-z]+(?: [A-Z][a-z]+)*)", text)
    date_match = re.search(r"Date Qualified[:\s]+(\d{4}-\d{2}-\d{2})", text)
    weapon_match = re.search(r"Weapon[:\s]+(M9|M4/M16|M500)", text)

    if name_match:
        data['name'] = name_match.group(1)
    if date_match:
        try:
            data['date_qualified'] = datetime.strptime(date_match.group(1), "%Y-%m-%d").date()
        except ValueError:
            pass
    if weapon_match:
        data['weapon'] = weapon_match.group(1)

    return data

def parse_ocr_text(text):
    import re
    parsed_data = {}

    # Example extraction patterns
    name_match = re.search(r'Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', text)
    rate_match = re.search(r'Rate[:\s]+([A-Z]{2,4})', text)
    weapon_match = re.search(r'Weapon[:\s]+(M4|M16|M9|M500)', text)
    category_match = re.search(r'Category[:\s]+(CAT I|CAT II|CAT III)', text)
    date_match = re.search(r'(?:Date\s+Qualified|Qualified\s+Date)[:\s]+(\d{2}/\d{2}/\d{4})', text)

    if name_match:
        parsed_data["name"] = name_match.group(1).strip()
    if rate_match:
        parsed_data["rate"] = rate_match.group(1).strip()
    if weapon_match:
        parsed_data["weapon"] = weapon_match.group(1).strip()
    if category_match:
        parsed_data["category"] = category_match.group(1).strip()
    if date_match:
        parsed_data["date_qualified"] = date_match.group(1).strip()

    return parsed_data
