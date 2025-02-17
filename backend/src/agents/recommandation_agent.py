from llama_index.core.base.llms.types import MessageRole, ChatMessage
import logging
import sys
import os
from brain import collect_homeloan_information
from src.agents.tools import detect_invalid_or_missing_fields
import json
from src.agents.recommandation import home_loan_recommandation

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def bot_agent_home_loan_recommandation_handle(history, message):
    """
    Handles the home loan recommendation workflow using the agent.
    """
    chat_history = convert_raw_messages_to_chat_messages(history)
    homeloan_application = collect_homeloan_information(chat_history, message)
    response             = detect_invalid_or_missing_fields(json.loads(homeloan_application))
    logging.info(f"Agent home loan recommendation response: {response}")
    if isinstance(response, dict):
        return home_loan_recommandation(response)
    return response