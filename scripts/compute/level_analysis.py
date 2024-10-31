"""Level analysis script."""

import argparse
from collections import Counter
from itertools import tee
import os
from pathlib import Path

import jsonlines
from utils import sanitize  # type: ignore


def main() -> None:
    level_dir = Path(os.environ["LEVEL_DIR"])
    train_level_dataset = jsonlines.open(level_dir / "train.jsonl")
    test_level_dataset, sanitized_test_level_dataset = tee(
        jsonlines.open(level_dir / "test.jsonl")
    )
    sanitized_test_level_dataset = sanitize(sanitized_test_level_dataset)

    train_c = Counter(e["max_level"] for e in train_level_dataset)
    test_c = Counter(e["max_level"] for e in test_level_dataset)
    sanitized_test_c = Counter(
        e["max_level"] for e in sanitized_test_level_dataset
    )
    print("category easy normal hard total")
    for name, c in zip(
        ["train", "test", "sanitized_test"], [train_c, test_c, sanitized_test_c]
    ):
        total = sum(c.values())
        print(name, end=" ")
        print(f"{c[1]} ({c[1]/total*100})", end=" ")
        print(f"{c[2]} ({c[2]/total*100})", end=" ")
        hard = c[3] + c[4] + c[5]
        print(f"{hard} ({hard/total*100})", end=" ")
        print(total)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main()
