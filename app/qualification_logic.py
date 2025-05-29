from datetime import datetime, timedelta

def evaluate_qualification(date_qualified: str, category: int, today: datetime) -> dict:
    """
    Evaluates qualification status based on OPNAVINST 3591.1G rules for Cat I–IV.

    Args:
        date_qualified (str): Date qualified, format 'YYYY-MM-DD'
        category (int): CAT I (1) through CAT IV (4)
        today (datetime): Today's date

    Returns:
        dict: {
            "qualified": bool,
            "sustainment_due": bool,
            "disqualified": bool,
            "expires_on": str (YYYY-MM-DD)
        }
    """
    if category != 2:
        raise ValueError("Only CAT II is supported at this stage.")

    qualified_date = datetime.strptime(date_qualified, "%Y-%m-%d")

    full_validity = qualified_date + timedelta(days=365)
    sustainment_due = qualified_date + timedelta(days=180)

    disqualified = today > full_validity
    sustainment_required = sustainment_due <= today <= full_validity

    return {
        "qualified": today <= full_validity,
        "sustainment_due": sustainment_required,
        "disqualified": disqualified,
        "expires_on": full_validity.strftime("%Y-%m-%d")
    }
