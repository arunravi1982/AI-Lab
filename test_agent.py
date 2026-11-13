import csv

from app import ask_agent
from evaluator import evaluate_response


def load_dataset():

    with open(
        "data/golden_dataset.csv",
        "r",
        encoding="utf-8"
    ) as file:

        return list(csv.DictReader(file))


def test_agent_responses():

    dataset = load_dataset()

    failures = []

    for row in dataset:

        actual = ask_agent(row["question"])

        status = evaluate_response(
            actual,
            row["expected_answer"]
        )

        if status == "FAIL":
            failures.append(
                f'{row["test_id"]}: Expected '
                f'{row["expected_answer"]}, got {actual}'
            )

    assert not failures, "\n".join(failures)