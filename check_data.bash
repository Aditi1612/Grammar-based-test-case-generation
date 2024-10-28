shopt -s globstar

for f in ${DATA_DIR}/{execution-summary,generation-result,grammar,parsing-result}/**/*.jsonl ${RAW_DATA_DIR}/{grammar,level,testcase}/**/*.jsonl; do
  filename=$(basename -- "$f" ".jsonl")
  if jq '.["name"]' -r $f | diff - "raw-data/problem-list/${filename}.txt" > /dev/null 2>&1; then
    echo -n $f
    echo " - OK"
  else
    echo -n $f
    echo " - Failed"
  fi
done;
