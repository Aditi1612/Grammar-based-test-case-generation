import os
import copy
from typing import (Any, Optional, cast, )

import jsonlines

from torch.utils.data import Dataset
from tokenizer import CountingContextFreeGrammarTokenizer as CcfgTokenizer


class MyDataset(Dataset):
    def __init__(self, path: Optional[os.PathLike] = None) -> None:
        if path is None:
            self.data: list[dict[str, Any]] = []
            return

        with jsonlines.open(path, 'r') as f:
            self.data = cast(
                list[dict[str, Any]],
                list(map(MyDataset.preprocess, f))
            )

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> dict[str, str]:
        """return the input ids, attention masks and target ids"""
        return self.data[index]

    def extend(self, dataset: list[dict[str, Any]]) -> None:
        self.data.extend(map(MyDataset.preprocess, dataset))

    @staticmethod
    def get_specification(description: str) -> str:
        description = MyDataset.replace_description(description)
        constraints_start_token = '\nconstraints\n'
        input_start_token = '\ninput\n'
        end_token = '\noutput\n'

        constraints_start = description.lower().find(constraints_start_token)
        input_start = description.lower().find(input_start_token)
        end = description.lower().find(end_token)

        constraints_start = (
            len(description) if constraints_start < 0 else constraints_start)
        input_start = len(description) if input_start < 0 else input_start

        start = min(constraints_start, input_start)
        start = 0 if start == len(description) else start
        end = len(description) if end < 0 else end

        specification = description[start:].strip()
        return specification

    @staticmethod
    def replace_description(description: str) -> str:
        description_replacements = [
            ('≤', '<='),
            ('\\leq', '<='),
            ('\\times', '*'),
        ]
        for old, new in description_replacements:
            description = description.replace(old, new)
        return description

    @staticmethod
    def partial_stringify(productions_or_constraints: list[str]) -> str:
        data = cast(list[str], productions_or_constraints)
        return f" {CcfgTokenizer.subseparator} ".join(data)

    @staticmethod
    def stringify(grammar: dict[str, list[str]]) -> str:
        productions = cast(list[str], grammar['productions'])
        constraints = cast(list[str], grammar['constraints'])
        return f" {CcfgTokenizer.separator} ".join([
            MyDataset.partial_stringify(productions),
            MyDataset.partial_stringify(constraints)
        ])

    @staticmethod
    def preprocess(obj: dict[str, Any]) -> dict[str, Any]:
        obj = copy.deepcopy(obj)

        description = obj['description']
        grammar = obj['grammar']
        obj['specification'] = MyDataset.get_specification(description)
        obj['stringified'] = MyDataset.stringify(grammar)
        return obj
