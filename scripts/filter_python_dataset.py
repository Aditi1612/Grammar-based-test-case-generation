"""Filter the dataset to only include Python3 solutions."""

from enum import IntEnum
import os
from pathlib import Path
from typing import Any

import jsonlines
from tqdm import tqdm


class LanguageType(IntEnum):
    UNKNOWN_LANGUAGE = 0
    PYTHON = 1
    CPP = 2
    PYTHON3 = 3
    JAVA = 4


def get_source_name(source: int) -> str:
    return [
        "UNKNOWN_SOURCE",
        "CODECHEF",
        "CODEFORCES",
        "HACKEREARTH",
        "CODEJAM",
        "ATCODER",
        "AIZU",
    ][source]


def has_python3_solution(data: dict[str, Any]) -> bool:
    languages: list[LanguageType] = (
        data["solutions"]["language"] + data["incorrect_solutions"]["language"]
    )
    return LanguageType.PYTHON3 in languages


def trim_solutions(
    solution_object: dict[str, Any],
) -> dict[str, list[str]]:

    languages = solution_object["language"]
    solutions = solution_object["solution"]

    trimmed_solutions = {
        "solution": [
            solution
            for language, solution in zip(languages, solutions)
            if language == LanguageType.PYTHON3
        ]
    }
    return trimmed_solutions


def trim(data: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "name",
        "description",
        "public_tests",
        "private_tests",
        "generated_tests",
    ]

    trimmed_data: dict[str, Any] = {k: data[k] for k in keys}
    trimmed_data["source"] = get_source_name(data["source"])
    trimmed_data["solutions"] = trim_solutions(data["solutions"])
    trimmed_data["incorrect_solutions"] = trim_solutions(
        data["incorrect_solutions"]
    )

    return trimmed_data


def main() -> None:
    raw_dataset_dir = Path("data/raw")
    dataset_dir = Path("data")

    os.makedirs(dataset_dir, exist_ok=True)

    for dataset_type in ["train", "test", "valid"]:
        raw_dataset_path = (
            raw_dataset_dir / f"code_contests_{dataset_type}.jsonl"
        )
        python_dataset_dir = dataset_dir / "unlabeled"
        os.makedirs(python_dataset_dir, exist_ok=True)
        python_dataset_path = (
            python_dataset_dir / f"code_contests_{dataset_type}_python.jsonl"
        )

        with jsonlines.open(raw_dataset_path, "r") as raw_dataset:
            python_dataset = filter(has_python3_solution, raw_dataset)
            trimmed_dataset = map(trim, python_dataset)

            tqdm_desc = f"Writing {python_dataset_path}"
            with jsonlines.open(python_dataset_path, "w") as writer:
                writer.write_all(tqdm(trimmed_dataset, desc=tqdm_desc))


if __name__ == "__main__":
    main()
