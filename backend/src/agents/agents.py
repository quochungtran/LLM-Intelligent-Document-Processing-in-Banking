from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.base.llms.types import MessageRole, ChatMessage
import logging
import sys
import os
from src.agents.tools import field_requirements, tools

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

formatted_valid_field = {"name": "Hung", "income": 50000, "credit_score": 100}
formatted_requirements = "\n".join([f"- `{field}`: {rule}" for field, rule in field_requirements.items()])

agent_prompt = f"""
You are an assistant specializing in home loan applications.
Your goal is to assist users by validating the required fields and collecting missing or invalid information. 

Your task is to validate the following mandatory fields in the user's input:
{formatted_requirements}

Action input should be:
{{"name": ..., "income": User's Income (numeric), "credit_score": User's Credit Score (numeric)}}

Steps:
1. Validate the user's input for these fields:
   - If a field is missing or invalid, immediately return the corresponding question for that field.
   - For example: If `income` is invalid or missing, return: "What is your annual income? Please provide it in numeric format."

2. Continue collecting and validating fields one at a time until all mandatory fields are valid.

3. Once all fields are valid, return the data in the following JSON format, as shown in the example:
{formatted_valid_field}

**Rules:**
- Only ask for one field at a time.
- If the `detect_invalid_or_missing_fields` tool outputs a valid JSON, immediately return that JSON as the final response.
- Do not modify, add context, or rephrase the output from the tool when it is valid.
"""

# Initialize LLM and Agent
llm = OpenAI(model="gpt-4")
asking_key_missing_agent = OpenAIAgent.from_tools(
    tools=tools,
    llm=llm,
    verbose=True,
    system_prompt=agent_prompt
)

# Utility functions
def convert_raw_messages_to_chat_messages(messages):
    """
    Converts a list of raw messages to ChatMessage instances.
    """
    chat_messages = []
    for message in messages:
        role = message.get("role", MessageRole.USER)
        content = message.get("content", "")
        chat_message = ChatMessage.from_str(content=content, role=role)
        chat_messages.append(chat_message)
    return chat_messages


def bot_agent_home_loan_recommandation_handle(history, question):
    """
    Handles the home loan recommendation workflow using the agent.
    """
    chat_history = convert_raw_messages_to_chat_messages(history)
    response = asking_key_missing_agent.chat(message=question, chat_history=chat_history)
    logging.info(f"Agent home loan recommendation response: {response}")
    return response
