"""Generate Python3 solutions from the code_contests dataset."""

from enum import IntEnum
import os
from pathlib import Path

import jsonlines
from tqdm import tqdm


class LanguageType(IntEnum):
    UNKNOWN_LANGUAGE = 0
    PYTHON = 1
    CPP = 2
    PYTHON3 = 3
    JAVA = 4


def main() -> None:
    dataset_dir = Path("data/unlabeled/")

    os.makedirs(dataset_dir, exist_ok=True)

    for dataset_type in ["train", "test", "valid"]:
        python_dataset_path = (
            dataset_dir / f"code_contests_{dataset_type}_python.jsonl"
        )

        with jsonlines.open(python_dataset_path, "r") as python_dataset:
            for data in tqdm(python_dataset):

                name = data["name"]

                for solution_type in ["solutions", "incorrect_solutions"]:

                    solutions = data[solution_type]["solution"]
                    solutions_dir = Path(
                        f"data/solutions/{solution_type}/{name}"
                    )
                    os.makedirs(solutions_dir, exist_ok=True)
                    for idx, solution in enumerate(solutions):
                        solution_path = solutions_dir / f"{idx}.py"
                        with open(solution_path, "w", encoding="utf-8") as f:
                            f.write(solution)


if __name__ == "__main__":
    main()
