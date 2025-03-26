import warnings
from tools.base import BaseTool
from sever_handling_pipeline import server_handler

warnings.filterwarnings("ignore")

class Revit_Saving_Directory_Tool(BaseTool):
    # This tool is intended to be triggered based on agent judgement,
    # not directly from a user request.
    require_llm_engine = False

    def __init__(self):
        super().__init__(
            tool_name="Revit_Saving_Directory_Tool",
            tool_description=(
                "Getting the saving directory for the exported files. "
                "This is executed based on the agent judgement—not the user request to do so. "
                "Don't execute this unless needed or planned to be executed."
            ),
            tool_version="1.0.0",
            input_types=
            {
                "message_for_user": "str - A message to be displayed to the user when the saving directory is determined."
            }, 
            output_type="str - A string containing the saving directory path for exported files.",
            demo_commands=[
                {
                    "command": 'execution = tool.execute(message_for_user="trying to get the saving directory..")',
                    "description": (
                        "Retrieve the saving directory for exported files as determined by agent judgement."
                    )
                }
            ],
        )

    def execute(self, message_for_user: str):
        """
        Get the saving directory for the exported files.
        Returns: str: A string containing the saving directory path for exported files.
        """
        request = f"GetSavingDirectory,(),{message_for_user}"
        response = server_handler.send_request(request)
        return response

    def get_metadata(self):
        metadata = super().get_metadata()
        return metadata

if __name__ == "__main__":
    tool = Revit_Saving_Directory_Tool()
    metadata = tool.get_metadata()
    print(metadata)