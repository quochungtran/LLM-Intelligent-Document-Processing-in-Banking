import logging
from llama_index.core.tools import QueryEngineTool, FunctionTool
from tool_info import ToolInfo, ToolType

# Configure logging
logging.basicConfig(level=logging.INFO)  # Adjust log level as needed
logger = logging.getLogger(__name__)


class AgentToolManager:
    """
    Manages tools for the agent, including QueryEngineTool and FunctionTool instances.
    """
    def __init__(self):
        """
        Initializes the tool manager with an empty list of tools.
        """
        self._tool_list = []

    def add_tool(self, tool_infos: list[ToolInfo]):
        """
        Creates and adds a tool based on the provided ToolInfo structure.

        :param tool_info: An instance of ToolInfo describing the tool.
        :return: The created tool, or None if creation failed.
        """
        for tool_info in tool_infos:
            if tool_info.tool_type == ToolType.QUERY_ENGINE:
                if not tool_info.query_engine or not tool_info.metadata:
                    logger.error(
                        "Failed to create QueryEngineTool: query engine and metadata are required."
                    )
                    return None
                tool = QueryEngineTool(query_engine=tool_info.query_engine, metadata=tool_info.metadata)

            elif tool_info.tool_type == ToolType.FUNCTION:
                if not tool_info.fn or not tool_info.name:
                    logger.error(
                        "Failed to create FunctionTool: function and name are required."
                    )
                    return None
                tool = FunctionTool.from_defaults(fn=tool_info.fn, name=tool_info.name)

            else:
                logger.error(f"Invalid tool_type '{tool_info.tool_type}'. Must be 'query_engine' or 'function'.")
                return None

            self._tool_list.append(tool)
            logger.info(f"Tool added successfully: {tool_info.tool_type} - {tool}")

    def get_tool_list(self):
        """
        Returns the list of tools managed by this instance.

        :return: A list of tools.
        """
        return self._tool_list
