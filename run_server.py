import os
import logging
from dotenv import load_dotenv
from typing import Dict, Optional, Any, List
import getpass
import os
import pandas as pd
import json
from tqdm import tqdm
from glob import glob
#Octotools 
from octotools.engine.openai import ChatOpenAI
import argparse
from tasks import solve


load_dotenv(override=True)

def get_server_handler():
    """
    Determines the environment and imports the appropriate server_handler.
    """
    environment = os.getenv("ENVIRONMENT")

    if environment == "client":
        from sever_handling_pipeline import server_handler
    elif environment == "local":
        from server_handling import server_handler
    else:
        raise EnvironmentError("ENVIRONMENT variable not set or invalid. Must be 'client' or 'local'.")
    
    return server_handler()

def _set_if_undefined(var: str) -> None:
    if os.environ.get(var):
        return
    os.environ[var] = getpass.getpass(var)

_set_if_undefined("OPENAI_API_KEY")
local_llm_engine = ChatOpenAI(enable_cache=False)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="agents_messages.txt",
    filemode='a'  # Append mode
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="communicating with Revit in order to get all the propsed categories available within the opened Revit document.")
    parser.add_argument("--llm_engine_name", default="gpt-4o", help="LLM engine name.")
    parser.add_argument("--max_tokens", type=int, default=4000, help="Maximum tokens for LLM generation.")
    parser.add_argument("--run_baseline_only", type=bool, default=False, help="Run only the baseline (no toolbox).")
    parser.add_argument("--task", default="", help="Task to run.")
    parser.add_argument("--data_file", default="data/data.json", help="Data file to run.")
    parser.add_argument("--task_description", default="communicating with Revit in order to get all the propsed categories available within the opened Revit document.", help="Task description.")
    parser.add_argument(
        "--output_types",
        default="base,final,direct",
        help="Comma-separated list of required outputs (base,final,direct)"
    )
    parser.add_argument("--enabled_tools", default="Revit_Cateogries_Handler_Tool", help="List of enabled tools.")
    parser.add_argument("--index", type=int, default=0, help="Index of the problem in the benchmark file.")
    parser.add_argument("--root_cache_dir", default="solver_cache", help="Path to solver cache directory.")
    parser.add_argument("--output_json_dir", default="results", help="Path to output JSON directory.")
    parser.add_argument("--max_steps", type=int, default=10, help="Maximum number of steps to execute.")
    parser.add_argument("--max_time", type=int, default=300, help="Maximum time allowed in seconds.")
    parser.add_argument("--verbose", type=bool, default=True, help="Enable verbose output.")
    return parser.parse_args()
    
def main():
    #global handler 
    #handler = get_server_handler()# Start the server and receive the initial message
    #handler.run_server()
    args = parse_arguments()
    solve.main(args)
    #question=handler.receive_initial_message()
    #full_prompt = create_prompt(system_message, question, output, out['answer'])
    #extraction = local_llm_engine(full_prompt)
    #print(extraction)
if __name__ == "__main__":
    main()


    
system_message = """
You are communicating with Revit in order to get all the propsed categories available within the opened Revit document.
"""
"""
exp_code = 'YOUR_EXPERIMENT_LABEL'

def create_prompt(demo_prompt, question, response, answer):
    demo_prompt = demo_prompt.strip()
    test_prompt = f"Question:\n{question}\n\nResponse:\n{response}\n\nCorrect Answer:\n{answer}"
    full_prompt = f"{demo_prompt}\n\n{test_prompt}\n\nCorrectness:"
    return full_prompt

# Agent exps
results_dir = f'../results/{exp_code}'
outputs = glob(f'{results_dir}/*.json')

use_col = 'direct_output'

items = []
for output in tqdm(outputs):
    item_id = os.path.splitext(os.path.basename(output))[0]
    with open(output, 'r') as f:
        out = json.load(f)

    output = out[use_col]

    question = out.get('query', out.get('question', ''))
    full_prompt = create_prompt(system_message, question, output, out['answer'])
    extraction = local_llm_engine(full_prompt)

    item = {
        'id': item_id,
        'question': question,
        'correct': out['answer'],
        'extracted_choice': extraction,
        'response': output,
        'use_col': use_col
    }
    items.append(item)
"""