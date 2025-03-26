"""
File: octotools/tools/revit_element_inspector/tool.py

This module implements the Revit_Element_Inspector_Tool.
The tool is designed to extract geometry and metadata from a Revit export file.
For demonstration purposes, the export file is assumed to be a JSON file
with a mapping from element IDs to their details.
"""

import os
import json
from octotools.tools.base import BaseTool

class Revit_Element_Inspector_Tool(BaseTool):
    # This tool operates locally so no LLM assistance is needed.
    require_llm_engine = False

    def __init__(self):
        super().__init__(
            tool_name="Revit_Element_Inspector_Tool",
            tool_description="Extracts geometry and metadata from a provided Revit element export file.",
            tool_version="1.0.0",
            input_types={
                "element_id": "str - The identifier of the Revit element (e.g., 'ELEM001').",
                "file_path": "str - The path to the Revit export file (e.g., a JSON file) containing element data."
            },
            output_type="dict - A dictionary with keys 'geometry' and 'metadata', or an error message.",
            demo_commands=[
                {
                    "command": 'execution = tool.execute(element_id="ELEM001", file_path="D:\Learning\AI\OctoTools\octotools2\octotools\dummy_revit_export.json")',
                    "description": "Extract data for element ELEM001 from an exported JSON file."
                }
            ]
        )

    def execute(self, element_id: str = None, file_path: str = None):
        # Validate inputs.
        if file_path is None:
            raise ValueError("The 'file_path' parameter is required.")
        if not os.path.exists(file_path):
            return {"error": f"File {file_path} does not exist."}

        try:
            with open(file_path, "r") as f:
                # Assume the file is JSON with a structure like:
                # { "ELEM001": {"geometry": {...}, "metadata": {...}}, ... }
                data = json.load(f)

            if element_id is not None:
                if element_id in data:
                    result = data[element_id]
                else:
                    return {"error": f"Element ID {element_id} not found in the file."}
            else:
                # If no element_id provided, return everything.
                result = data

            return result
        except Exception as e:
            return {"error": str(e)}

# For testing purpose only.
if __name__ == "__main__":
    # Create a dummy exported file for testing.
    dummy_data = {
        "ELEM001": {
            "geometry": {"length": 12.5, "width": 3.2, "height": 4.1},
            "metadata": {"material": "Aluminum", "element_type": "Curtain Wall"}
        },
        "ELEM002": {
            "geometry": {"length": 8.0, "width": 2.5, "height": 3.0},
            "metadata": {"material": "Glass", "element_type": "Window"}
        }
    }
    dummy_file = "dummy_revit_export.json"
    with open(dummy_file, "w") as f:
        json.dump(dummy_data, f, indent=4)

    tool = Revit_Element_Inspector_Tool()
    # Test with a valid element_id.
    result = tool.execute(element_id="ELEM001", file_path=dummy_file)
    print("Test result for element ELEM001:")
    print(json.dumps(result, indent=4))

    # Test with an invalid element_id.
    result_invalid = tool.execute(element_id="ELEMXXX", file_path=dummy_file)
    print("Test result for an invalid element:")
    print(json.dumps(result_invalid, indent=4))
