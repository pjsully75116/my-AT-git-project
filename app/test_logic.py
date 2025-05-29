from datetime import datetime, timedelta
from app.qualification_logic import evaluate_qualification

today = datetime.today()
print(f"\nToday is: {today.strftime('%Y-%m-%d')}")

test_cases = [
    ((today - timedelta(days=90)).strftime("%Y-%m-%d"), "Recent qual — fully valid"),
    ((today - timedelta(days=210)).strftime("%Y-%m-%d"), "In sustainment window"),
    ((today - timedelta(days=360)).strftime("%Y-%m-%d"), "Barely within 1 year — sustainment due"),
    ((today - timedelta(days=365)).strftime("%Y-%m-%d"), "Expired exactly today"),
    ((today - timedelta(days=425)).strftime("%Y-%m-%d"), "Well past expiration — disqualified"),
]

for date_str, description in test_cases:
    result = evaluate_qualification(date_str, 2, today)
    print(f"\nTest: {description}")
    print(f"Qualified on: {date_str}")
    for key, value in result.items():
        print(f"{key}: {value}")
