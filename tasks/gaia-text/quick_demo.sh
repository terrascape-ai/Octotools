#!/bin/bash

############ [1] Single Run ############
PROJECT_DIR="./"

LABEL="quick_demo"

TASK="gaia-text"
DATA_FILE="$TASK/data/data.json"
LOG_DIR="$TASK/logs/$LABEL"
OUT_DIR="$TASK/results/$LABEL"
CACHE_DIR="$TASK/cache"

LLM="gpt-4o"

ENABLED_TOOLS="Python_Code_Generator_Tool,Google_Search_Tool,Wikipedia_Knowledge_Searcher_Tool,URL_Text_Extractor_Tool,Generalist_Solution_Generator_Tool"

INDEX=0 

python solve.py \
--index $INDEX \
--task $TASK \
--data_file $DATA_FILE \
--llm_engine_name $LLM \
--root_cache_dir $CACHE_DIR \
--output_json_dir $OUT_DIR \
--output_types direct \
--enabled_tools "$ENABLED_TOOLS" \
--max_time 300
