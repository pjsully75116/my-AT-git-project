from datetime import datetime
from qualification_logic import evaluate_qualification

# Example: qualified on Nov 1, 2023
test_date = "2023-11-01"
category = 2
today = datetime.today()

result = evaluate_qualification(test_date, category, today)

print("Qualification Evaluation:")
for key, value in result.items():
    print(f"{key}: {value}")
