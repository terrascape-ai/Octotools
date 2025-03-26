from octotools.tools.base import BaseTool
from sever_handling_pipeline import server_handler
import warnings

warnings.filterwarnings("ignore")

class Revit_Cateogries_Handler_Tool(BaseTool):
    # This tool operates locally so no LLM assistance is needed.
    require_llm_engine = False

    def __init__(self):
        super().__init__(
            tool_name="Revit_Cateogries_Handler_Tool",
            tool_description="A tool that communicates with Revit to the available model categories",
            tool_version="1.0.0",
            input_types={}, 
            output_type="str - A string that contains the Revit response containing all the Revit available categoris",
            demo_commands=[
                {
                    "command": 'execution = tool.execute()',
                    "description": "Send request to Revit To retrieve all the available categories within this Revit docuement"
                }
            ],
        )
    
    def execute(self):
        """
        Communicates with Revit to the available model categories"
        Returns:"str - A string that contains the Revit response containing all the Revit available categoris"
        """
        
        request = "GetCategoriesForCurrentDocument,(),Fetching model to get model categories" 
        response = server_handler.send_request(request) 
        return response
    
    def get_metadata(self):
        """
        Returns the metadata for the Wikipedia_Knowledge_Searcher_Tool.

        Returns:
            dict: A dictionary containing the tool's metadata.
        """
        metadata = super().get_metadata()
        return metadata
if __name__ == "__main__":
    tool = Revit_Cateogries_Handler_Tool()
    metadata = tool.get_metadata()
    print(metadata)