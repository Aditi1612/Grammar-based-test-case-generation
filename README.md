# Neural Translation of Input Specifications into Formal Grammars for Test Case Generation

by Anonymous

This repo provides the source code & data of our work.

## Abstract

> Test cases are crucial for ensuring the program's correctness and evaluating
> performance in programming. The high diversity of test cases within
> constraints is necessary to distinguish between correct and incorrect
> answers. Automated source code generation is currently a popular area due to
> the inefficiency of manually generating test cases. Recent attempts involve
> generating conditional cases from problem descriptions using deep-learning
> models that learn from source code. However, this task requires a combination
> of complex skills such as extracting syntactic and logical constraints for a
> given test case from a problem, and generating test cases that satisfy the
> constraints. In this work, we introduce a modified context-free grammar that
> explicitly represents the syntactical and logical constraints embedded within
> programming problems. Our innovative framework for automated test case
> generation separates restriction extraction from test case generation,
> simplifying the task for the model. We compare diverse methods for neural
> translation of input specifications into formal grammars.

## Usage

### Environment setup

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ source .envrc
$ pip install -r requirements.txt
```

### Data download

This section is optional. If you don't want to train the model, you can skip
this section and start from the section ["Reproducing the evaluation
results"](#reproducing-the-evaluation-results).

The following command will create `data/{raw,solutions,unlabeled}`.

```bash
$ make prepare-dataset
```

### Training the CcfgT5 model

The following command will train the CcfgT5 model. The trained model will be
saved in `saved/ccfg-t5/`.

```bash
$ python train.py
```

Run the following command to generate grammars using the trained model.

```bash
$ mv ./raw-data/grammar/ccfg-t5 ./ccfg-t5.backup
$ make $(pwd)/data/grammar/ccfg-t5/beam-{1,10}/test.jsonl MODEL=<checkpoint>
```

### Reproducing the evaluation results

Place solution files in `data/solutions/{solutions,incorrect_solutions}/`.
Then, `make all` command will reproduce the following evaluation results.

```bash
 data
 ├── execution-summary
 │   ├── code-contest/{generated,private,public}/test.jsonl
 │   ├── direct/{gemini,gpt}/test.jsonl
 │   ├── fuzzing/{private,public}/test.jsonl
 │   └── grammar
 │       ├── ccfg-t5/{beam-1,beam-10}/test.jsonl
 │       ├── gemini/{1-shot,5-shot}/test.jsonl
 │       ├── gpt/{1-shot,5-shot}/test.jsonl
 │       └── ground-truth/test.jsonl
 ├── generation-result
 │   ├── code-contest/{generated,private,public}/test.jsonl
 │   ├── direct/{gemini,gpt}/test.jsonl
 │   ├── fuzzing/{private,public}/test.jsonl
 │   └── grammar
 │       ├── ccfg-t5/{beam-1,beam-10}/test.jsonl
 │       ├── gemini/{1-shot,5-shot}/test.jsonl
 │       ├── gpt/{1-shot,5-shot}/test.jsonl
 │       └── ground-truth/test.jsonl
 └── parsing-result
        ├── ccfg-t5/{beam-1,beam-10}/test.jsonl
        ├── gemini/{1-shot,5-shot}/test.jsonl
        ├── gpt/{1-shot,5-shot}/test.jsonl
        └── ground-truth/test.jsonl
```

To see the analysis, run the following commands.

```bash
$ bash scripts/print/{validity,effectiveness}.sh
$ bash scripts/print/{validity,effectiveness}_level.sh
$ bash scripts/print/effectiveness_length{,_acc,_comb}.sh
$ bash scripts/print/{exact_match,bleu_score}.sh
$ bash scripts/print/generality.sh
```

## Citation

Not available.

## License

All source code is made available under a BSD 3-clause license. You can freely
use and modify the code, without warranty, so long as you provide attribution
to the authors. See `LICENSE.md` for the full license text.
