shopt -s globstar

for file in ${DATA_DIR}/execution-summary/grammar/**/*.jsonl; do
  echo "$file"
  generation=${file/execution-summary/generation-result}
  python scripts/compute/effectiveness_set_length_combination.py \
    --execution-summary "$file" \
    --generation-result "$generation"
  echo
done
