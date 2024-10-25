"""Case Study"""

import os
from pathlib import Path

import jsonlines


def main() -> None:
    ground_truth_generation_results = jsonlines.open(
        Path(os.environ["GROUND_TRUTH_GENERATION_RESULT"]), "r"
    )
    public_generation_results = jsonlines.open(
        Path(os.environ["PUBLIC_GENERATION_RESULT"]), "r"
    )
    private_generation_results = jsonlines.open(
        Path(os.environ["PRIVATE_GENERATION_RESULT"]), "r"
    )
    ground_truth_parsing_results = jsonlines.open(
        Path(os.environ["GROUND_TRUTH_PARSING_RESULT"]), "r"
    )
    ground_truth_execution_summaries = jsonlines.open(
        Path(os.environ["GROUND_TRUTH_EXECUTION_SUMMARY"]), "r"
    )

    for (
        ground_truth_generation_result,
        public_generation_result,
        private_generation_result,
        ground_truth_parsing_result,
        ground_truth_execution_summary,
    ) in zip(
        ground_truth_generation_results,
        public_generation_results,
        private_generation_results,
        ground_truth_parsing_results,
        ground_truth_execution_summaries,
    ):
        name = ground_truth_generation_result["name"]
        assert name == public_generation_result["name"]
        assert name == private_generation_result["name"]
        assert name == ground_truth_parsing_result["name"]
        assert name == ground_truth_execution_summary["name"]

        flag = False
        for result in [
            public_generation_result["results"],
            private_generation_result["results"],
        ]:
            if not all(e["parsable"] for e in result):
                flag = True
                break

        if flag:
            print(name)
            print("Maybe grammar issue")
            print()
            continue

        if len(ground_truth_generation_result["results"]) == 0:
            print(name)
            print("Fails to generate test cases")
            print()
            continue

        flag = False
        for result in [
            ground_truth_generation_result["results"],
            ground_truth_parsing_result["results"],
        ]:
            if not all(e["parsable"] for e in result):
                flag = True
                break

        if flag:
            print(name)
            print("Maybe implementation issue")
            print()
            continue

        summary_results = ground_truth_execution_summary["results"]
        assert len(summary_results) > 0
        if len(summary_results[0]["incorrect_results"]) == 0:
            print(name)
            print("There is no incorrect solutions")
            print()
            continue


if __name__ == "__main__":
    main()
