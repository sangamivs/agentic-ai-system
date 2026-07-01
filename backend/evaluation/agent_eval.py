import json
import requests

API_URL = "http://127.0.0.1:8000/api/v1/chat"

with open("backend/evaluation/test_cases.json", "r") as f:
    test_cases = json.load(f)

passed = 0

for tc in test_cases:

    print("=" * 60)
    print("INPUT :", tc["input"])

    response = requests.post(
        API_URL,
        json={"message": tc["input"]}
    )

    if response.status_code != 200:
        print("❌ API Error:", response.status_code)
        continue

    result = response.json()

    answer = result["answer"]

    tool_calls = result.get("tool_calls_made", 0)

    print("Answer:")
    print(answer)

    print("Tool Calls:", tool_calls)

    response_ok = tc["expected_contains"].lower() in answer.lower()

    if response_ok:
        print("✅ Response Correct")
        passed += 1
    else:
        print("❌ Response Incorrect")

print("\n" + "=" * 60)
print(f"FINAL SCORE : {passed}/{len(test_cases)}")