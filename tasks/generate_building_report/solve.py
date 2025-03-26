"""
File: tasks/generate_building_report/solve.py

This script demonstrates a high-level task solver that leverages octotools to
generate a building report. It uses the new Revit_Element_Inspector_Tool along with
other octotools components (Planner, Memory, Executor) to extract data from an exported
Revit file and compile the report. In this version every planning step is executed via
actual LLM calls (instead of simulations).
"""

import os
import sys
import json
import argparse
import time

# Add the project root to sys.path so that octotools modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# Import octotools core components
from octotools.models.initializer import Initializer
from octotools.models.planner import Planner
from octotools.models.memory import Memory
from octotools.models.executor import Executor
from octotools.models.utlis import make_json_serializable_truncated

# Import the Generalist tool for base response generation
from octotools.tools.generalist_solution_generator.tool import Generalist_Solution_Generator_Tool


class Solver:
    def __init__(
        self,
        task: str,
        data_file: str,
        task_description: str,
        output_types: str = "base,final,direct",
        index: int = 0,
        verbose: bool = True,
        max_steps: int = 5,
        max_time: int = 60,
        max_tokens: int = 4000,
        output_json_dir: str = "results",
        root_cache_dir: str = "solver_cache",
        enabled_tools: str = "Revit_Element_Inspector_Tool,Generalist_Solution_Generator_Tool"
    ):
        self.task = task
        self.data_file = data_file
        self.task_description = task_description
        self.index = index
        self.verbose = verbose
        self.max_steps = max_steps
        self.max_time = max_time
        self.max_tokens = max_tokens
        self.output_json_dir = output_json_dir
        self.root_cache_dir = root_cache_dir
        self.output_types = output_types.lower().split(',')

        self.enabled_tools = [e.strip() for e in enabled_tools.split(",")]

        # Load benchmark data (assume JSON file with one or more test problems)
        self.benchmark_data = self.load_benchmark_data()# this can read the user query data, or we can append the user query data to the benchmark data at a gieven pid 

    def load_benchmark_data(self):
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        # Prepend the task description (if available) to each query.
        for problem in data:
            if self.task_description:
                problem['query'] = f"Task: {self.task_description}\n" + problem.get('query', '')
        return data

    def solve_single_problem(self, index: int):
        # Set up the cache directory for the executor.
        cache_dir = os.path.join(self.root_cache_dir, f"{index}")
        
        # Create output directory if not present.
        os.makedirs(self.output_json_dir, exist_ok=True)
        output_file = os.path.join(self.output_json_dir, f"output_{index}.json")

        # Retrieve the problem information.
        problem = self.benchmark_data[index]
        query = problem.get("query", "")
        image_path = problem.get("image", "")
        pid = problem.get("pid", index)
        answer = problem.get("answer", "")

        if self.verbose:
            print("#" * 80)
            print(f"Problem {index} / PID {pid}")
            print("Query:")
            print(query)
            if image_path:
                print(f"Image: {image_path}")
            print("Reference Answer:")
            print(answer) # this is the answer from the json file
            print("#" * 80)

        # Prepare base output details.
        json_data = {
            "pid": pid,
            "query": query,
            "image": image_path,
            "answer": answer,
        }
        """
        # --- Base Response Generation using the Generalist Tool ---
        generalist_tool = Generalist_Solution_Generator_Tool(model_string="gpt-4o-mini")
        if image_path and os.path.exists(image_path):
            base_response = generalist_tool.execute(prompt=query, image=image_path)
        else:
            base_response = generalist_tool.execute(prompt=query)
        json_data["base_response"] = base_response
        if self.verbose:
            print("Base Response (from Generalist Tool):")
            print(base_response)
        # --- End Base Response Generation ---

        # If only a base response is requested, then save and return.
        if set(self.output_types) == {"base"}:
            with open(output_file, 'w') as f:
                json.dump(json_data, f, indent=4)
            print("Output saved to:", output_file)
            return
        """
        # Initialize core components
        initializer = Initializer(enabled_tools=self.enabled_tools, model_string="gpt-4o-mini")
        planner = Planner(
            llm_engine_name="gpt-4o-mini",
            toolbox_metadata=initializer.toolbox_metadata,
            available_tools=initializer.available_tools,
        )
        memory = Memory()
        executor = Executor(
            llm_engine_name="gpt-4o-mini",
            root_cache_dir=cache_dir
        )
        executor.set_query_cache_dir(cache_dir)

        # Perform query analysis via the Planner.
        query_analysis = planner.analyze_query(query, image_path)
        json_data["query_analysis"] = query_analysis
        if self.verbose:
            print("Query Analysis:")
            print(query_analysis)

        start_time = time.time()
        step_count = 0

        # Main iterative planning–execution loop.
        while step_count < self.max_steps and (time.time() - start_time) < self.max_time:
            step_count += 1
            if self.verbose:
                print("=" * 50)
                print(f"Step {step_count}")

            # --- Real Next-Step Generation ---
            # Call the planner (using LLM) to produce the next step.
            next_step = planner.generate_next_step(
                question=query,
                image=image_path,
                query_analysis=query_analysis,
                memory=memory,
                step_count=step_count,
                max_step_count=self.max_steps
            )
            # Extract structured fields: context, sub_goal, and tool_name.
            context, sub_goal, tool_name = planner.extract_context_subgoal_and_tool(next_step)
            if self.verbose:
                print("Next Step generated by Planner:")
                print("Context:", context)
                print("Sub-goal:", sub_goal)
                print("Tool selected:", tool_name)
            # --- End Next-Step Generation ---

            # --- Real Tool Command Generation ---
            # Use the executor's method to generate a tool command for the selected tool.
            tool_metadata = planner.toolbox_metadata.get(tool_name, {})
            tool_command = executor.generate_tool_command(query, image_path, context, sub_goal, tool_name, tool_metadata)
            # Extract explanation and formatted command.
            explanation, command = executor.extract_explanation_and_command(tool_command)
            if self.verbose:
                print("Tool Command generated by Executor:")
                print("Explanation:")
                print(explanation)
                print("Command:")
                print(command)
            # --- End Tool Command Generation ---

            # --- Tool Execution ---
            result = executor.execute_tool_command(tool_name, command)
            result = make_json_serializable_truncated(result)
            if self.verbose:
                print("Tool Execution Result:")
                print(json.dumps(result, indent=4))
            # --- End Tool Execution ---

            # Update memory with the action of this step.
            memory.add_action(step_count, tool_name, sub_goal, command, result)

            # --- Real Stop Verification ---
            # Ask the Planner to verify the memory—whether enough information has been gathered.
            stop_verification = planner.verificate_context(query, image_path, query_analysis, memory)
            conclusion = planner.extract_conclusion(stop_verification)
            if self.verbose:
                print("Stopping Verification:")
                print(stop_verification)
                print("Conclusion extracted:", conclusion)
            if conclusion == 'STOP':
                if self.verbose:
                    print("Stopping condition met. Exiting planning loop.")
                break
            # --- End Stop Verification ---
        
        # Append memory and execution statistics.
        json_data["memory"] = memory.get_actions()
        json_data["step_count"] = step_count
        json_data["execution_time"] = round(time.time() - start_time, 2)

        # --- Final Outputs Generation ---
        # In a complete system, the Planner would now generate a final output.
        final_output = planner.generate_final_output(query, image_path, memory)
        direct_output = planner.generate_direct_output(query, image_path, memory)
        json_data["final_output"] = final_output
        json_data["direct_output"] = direct_output
        if self.verbose:
            print("Final Output from Planner:")
            print(final_output)
            print("Direct Output from Planner:")
            print(direct_output)
        # --- End Final Outputs Generation ---

        with open(output_file, 'w') as f:
            json.dump(json_data, f, indent=4)
        print("\n==> Output saved to:", output_file)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Building Report Using octotools")
    parser.add_argument("--data_file", type=str, default="tasks\generate_building_report\data\sample_report_data.json",
                        help="JSON file with test problems")
    parser.add_argument("--task_description", type=str, default="Extract detailed geometry and material properties for curtain wall elements.",
                        help="Task description")
    parser.add_argument("--index", type=int, default=0, help="Index of the problem to solve")
    parser.add_argument("--output_json_dir", type=str, default="results", help="Directory to save outputs")
    parser.add_argument("--max_steps", type=int, default=5, help="Maximum number of planning steps")
    parser.add_argument("--max_time", type=int, default=60, help="Maximum execution time (seconds)")
    parser.add_argument("--verbose", type=bool, default=True, help="Enable verbose output")
    parser.add_argument("--enabled_tools", type=str, default="Revit_Element_Inspector_Tool,Generalist_Solution_Generator_Tool",
                        help="Comma-separated list of enabled tool names")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    solver = Solver(
        task="Generate_Building_Report",
        data_file=args.data_file,
        task_description=args.task_description,
        output_types="base,final,direct",
        index=args.index,
        verbose=args.verbose,
        max_steps=args.max_steps,
        max_time=args.max_time,
        max_tokens=4000,
        output_json_dir=args.output_json_dir,
        root_cache_dir="solver_cache",
        enabled_tools=args.enabled_tools
    )
    solver.solve_single_problem(args.index)
