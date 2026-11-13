import csv
import os

from app import ask_agent


def evaluate_response(actual, expected):

    actual = actual.lower().strip()
    expected = expected.lower().strip()

    if expected in actual:
        return "PASS"

    return "FAIL"


def run_evaluation():

    results = []

    with open(
        "data/golden_dataset.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            question = row["question"]
            expected = row["expected_answer"]

            print("\nTesting:", row["test_id"])

            actual = ask_agent(question)

            status = evaluate_response(
                actual,
                expected
            )

            result = {
                "test_id": row["test_id"],
                "question": question,
                "expected": expected,
                "actual": actual,
                "status": status
            }

            results.append(result)

            print("Expected:", expected)
            print("Actual:", actual)
            print("Status:", status)

    os.makedirs("outputs", exist_ok=True)

    with open(
        "outputs/evaluation_report.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "test_id",
            "question",
            "expected",
            "actual",
            "status"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    passed = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    failed = len(results) - passed

    print("\n========== EVALUATION SUMMARY ==========")
    print("Total Tests:", len(results))
    print("Passed:", passed)
    print("Failed:", failed)

    if results:
        print(
            "Pass Rate:",
            round((passed / len(results)) * 100, 2),
            "%"
        )

    print("\nReport saved in outputs/evaluation_report.csv")


if __name__ == "__main__":
    run_evaluation()