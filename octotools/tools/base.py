# octotools/tools/base.py

import os
import sys
# Add the project root to sys.path so that octotools modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from octotools.engine.openai import ChatOpenAI

class BaseTool:
    """
    A base class for building tool classes that perform specific tasks, such as image processing or text detection.
    """

    require_llm_engine = False  # Default is False, tools that need LLM should set this to True

    def __init__(self, tool_name=None, tool_description=None, tool_version=None, input_types=None, output_type=None, demo_commands=None, output_dir=None, user_metadata=None, model_string=None):
        """
        Initialize the base tool with optional metadata.

        Parameters:
            tool_name (str): The name of the tool.
            tool_description (str): A description of the tool.
            tool_version (str): The version of the tool.
            input_types (dict): The expected input types for the tool.
            output_type (str): The expected output type for the tool.
            demo_commands (list): A list of example commands for using the tool.
            output_dir (str): The directory where the tool should save its output (optional).
            user_metadata (dict): Additional metadata specific to user needs (optional).
            model_string (str): The model string for the LLM engine (optional, only used if require_llm_engine is True).
        """
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = tool_version
        self.input_types = input_types
        self.output_type = output_type
        self.demo_commands = demo_commands
        self.output_dir = output_dir
        self.user_metadata = user_metadata
        self.model_string = model_string

    def set_metadata(self, tool_name, tool_description, tool_version, input_types, output_type, demo_commands, user_metadata=None):
        """
        Set the metadata for the tool.

        Parameters:
            tool_name (str): The name of the tool.
            tool_description (str): A description of the tool.
            tool_version (str): The version of the tool.
            input_types (dict): The expected input types for the tool.
            output_type (str): The expected output type for the tool.
            demo_commands (list): A list of example commands for using the tool.
            user_metadata (dict): Additional metadata specific to user needs (optional).
        """
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_version = tool_version
        self.input_types = input_types
        self.output_type = output_type
        self.demo_commands = demo_commands
        self.user_metadata = user_metadata

    def get_metadata(self):
        """
        Returns the metadata for the tool.

        Returns:
            dict: A dictionary containing the tool's metadata.
        """
        metadata = {
            "tool_name": self.tool_name,
            "tool_description": self.tool_description,
            "tool_version": self.tool_version,
            "input_types": self.input_types,
            "output_type": self.output_type,
            "demo_commands": self.demo_commands,
            "require_llm_engine": self.require_llm_engine,
        }
        if self.user_metadata:
            metadata["user_metadata"] = self.user_metadata
        return metadata

    def set_custom_output_dir(self, output_dir):
        """
        Set a custom output directory for the tool.

        Parameters:
            output_dir (str): The new output directory path.
        """
        self.output_dir = output_dir

    def set_llm_engine(self, model_string):
        """
        Set the LLM engine for the tool.

        Parameters:
            model_string (str): The model string for the LLM engine.
        """
        self.model_string = model_string

    def execute(self, *args, **kwargs):
        """
        Execute the tool's main functionality. This method should be overridden by subclasses.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the execute method.")