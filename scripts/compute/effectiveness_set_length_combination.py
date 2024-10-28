"""Set-based effectiveness respect to the length of test cases, for all
combinations.
"""

import argparse
from itertools import chain, combinations
from pathlib import Path

import jsonlines  # type: ignore
import numpy as np  # type: ignore
from utils import sanitize  # type: ignore


def main(
    execution_summary_path: Path,
    generation_path: Path,
) -> None:

    summaries = jsonlines.open(execution_summary_path)
    generation_results = jsonlines.open(generation_path)

    count = 0
    degrees = [0, 1, 2]
    combination_to_effectiveness_list: dict[tuple[int, int], list[float]] = {
        combination: [] for combination in combinations(degrees, 2)
    }
    it = sanitize(zip(summaries, generation_results))
    for summary, generation_result in it:
        count += 1

        assert summary["name"] == generation_result["name"]

        testcase_summaries = summary["results"]
        testcase_generations = generation_result["results"]
        validities = [e["parsable"] for e in testcase_generations]
        assert len(testcase_summaries) == len(validities)

        # We consider the effectiveness of failed grammar as 0
        if len(testcase_summaries) == 0:
            for (
                effectiveness_list
            ) in combination_to_effectiveness_list.values():
                effectiveness_list.append(0.0)
            continue

        # We consider the effectiveness of an invalid set of testcase as 0
        if not all(validities):
            for (
                effectiveness_list
            ) in combination_to_effectiveness_list.values():
                effectiveness_list.append(0.0)
            continue

        # Remove a short test case
        if len(testcase_summaries) == 31:
            testcase_summaries.pop(1)

        assert len(testcase_summaries) == 30

        degree_to_testcase_summaries_list = {
            degree: testcase_summaries[degree * 10 : (degree + 1) * 10]
            for degree in degrees
        }

        for combination_items in combinations(
            list(degree_to_testcase_summaries_list.items()), 2
        ):
            # Initialize expectation of incorrect results
            total_incorrect_results = [True] * len(
                testcase_summaries[0]["incorrect_results"]
            )

            combination = (combination_items[0][0], combination_items[1][0])
            testcase_summaries = (
                combination_items[0][1] + combination_items[1][1]
            )
            for testcase_summary in testcase_summaries:
                incorrect_results = testcase_summary["incorrect_results"]
                assert len(incorrect_results) > 0

                for i, incorrect_result in enumerate(incorrect_results):
                    total_incorrect_results[i] &= incorrect_result

            effectiveness = 1 - sum(total_incorrect_results) / len(
                total_incorrect_results
            )
            combination_to_effectiveness_list[combination].append(effectiveness)

    for (
        combination,
        effectiveness_list,
    ) in combination_to_effectiveness_list.items():
        effectiveness = float(np.average(effectiveness_list))

        print("total used combination effectiveness")
        print(count, len(effectiveness_list), combination, effectiveness * 100)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution-summary", type=Path)
    parser.add_argument("--generation-result", type=Path)

    args = parser.parse_args()
    main(
        args.execution_summary,
        args.generation_result,
    )
