#!/bin/bash

############ [1] Batching Run ############
PROJECT_DIR="./"

############
LABEL="gpt4o_baseline"

THREADS=8
TASK="gameof24"
DATA_FILE="$TASK/data/data.json"
LOG_DIR="$TASK/logs/$LABEL"
OUT_DIR="$TASK/results/$LABEL"

LLM="gpt-4o-mini"

############

cd $PROJECT_DIR
mkdir -p $LOG_DIR

# Define the array of specific indices
indices=($(seq 100 107))

# Skip indices if the output file already exists
new_indices=()
for i in "${indices[@]}"; do
    if [ ! -f "$OUT_DIR/output_$i.json" ]; then
        new_indices+=($i)
    else
        echo "Output file already exists: $OUT_DIR/output_$i.json"
    fi
done
indices=("${new_indices[@]}")
echo "Final indices: ${indices[@]}"

# Check if indices array is empty
if [ ${#indices[@]} -eq 0 ]; then
    echo "All tasks completed."
else
    # Function to run the task for a single index
    run_task() {
        local i=$1
        echo "Running task for index $i"
        python solve.py \
        --index $i \
        --task $TASK \
        --data_file $DATA_FILE \
        --llm_engine_name $LLM \
        --output_json_dir $OUT_DIR \
        --output_types base
        2>&1 | tee $LOG_DIR/$i.log
        echo "Completed task for index $i"
        echo "------------------------"
    }

    # Export the function and variables so they can be used by parallel
    export -f run_task
    export TASK DATA_FILE LOG_DIR OUT_DIR LLM

    # Run the tasks in parallel using GNU Parallel
    echo "Starting parallel execution..."
    parallel -j $THREADS run_task ::: "${indices[@]}"
    echo "All tasks completed."
fi

############ [2] Calculate Scores ############
cd $PROJECT_DIR

RESPONSE_TYPE="base_response"
python $TASK/calculate_score.py \
--data_file $DATA_FILE \
--result_dir $OUT_DIR \
--response_type $RESPONSE_TYPE \
--output_file "final_results_$RESPONSE_TYPE.json" \
| tee "$OUT_DIR/final_score_$RESPONSE_TYPE.log"

