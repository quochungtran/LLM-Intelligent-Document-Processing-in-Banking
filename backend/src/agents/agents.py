from llama_index.core.tools import ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

from rag.documentLoader import *
from agent_tool_manager import AgentToolManager
from tool_info import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

class BaseAgent:
    """
    Represents an agent that uses tools to perform tasks via an LLM model.
    """
    def __init__(self, llm_model, tool_manager: AgentToolManager):
        """
        Initializes the agent with a query engine, LLM model, and tool manager.
        :param llm_model: The language model for processing queries.
        :param tool_manager: An instance of AgentToolManager to manage tools.
        """
        self._llm_model = llm_model
        self._tool_manager = tool_manager

        # Initialize the agent with tools from the tool manager
        self._agent = OpenAIAgent.from_tools(
            tools=tool_manager.get_tool_list(), llm_model=llm_model, verbose=True
        )

    def get_agent(self):
        """
        Returns the underlying OpenAIAgent instance.
        
        :return: The OpenAIAgent instance.
        """
        return self._agent
    
    def get_tool_manager(self):
        return self._tool_manager


if __name__ == "__main__":

    vinfast_loader = DocumentLoader(loader=WikipediaReader(), pages=["Vinfast"])
    _, vinfast_query_engine = vinfast_loader.generate_query_engine()

    vinamilk_loader = DocumentLoader(loader=WikipediaReader(), pages=["Vinamilk"])
    _, vinamilk_query_engine = vinamilk_loader.generate_query_engine()

    toolManager = AgentToolManager()

    tool_info_query_vinfast = ToolInfo(
        tool_type=ToolType.QUERY_ENGINE,
        query_engine=vinfast_query_engine,
        metadata=ToolMetadata(
                                name="Vinfast_data",    
                                description=(
                                            "Provides information about Vinfast company. "
                                            "Use a detailed plain text question as input to the tool."
                                ),
                            ),
                        )
    tool_info_query_vinamilk = ToolInfo(
        tool_type=ToolType.QUERY_ENGINE,
        query_engine=vinamilk_query_engine,
        metadata=ToolMetadata(
                                name="Vinamilk_data",    
                                description=(
                                            "Provides information about Vinamilk company. "
                                            "Use a detailed plain text question as input to the tool."
                                ),
                            ),
                        )

    toolManager.add_tool(tool_infos=[tool_info_query_vinfast, tool_info_query_vinamilk])
    agent = Agent(llm_model = OpenAI(model="gpt-4o-mini", temperature=0.0), tool_manager=toolManager)
    agent.get_agent().chat_repl()