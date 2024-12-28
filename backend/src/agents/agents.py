from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.base.llms.types import MessageRole, ChatMessage
import logging
import sys
import os
from src.agents.tools import field_requirements, tools
import json
from src.agents.recommandation import home_loan_recommandation

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

formatted_valid_field = {"name": "Hung", 
                         "income": 50000, 
                         "loan_amount": 100,
                         "property_value": 405000.0,
                         "loan_term": 360.0,
                         "loan_purpose": "Home purchase"
                        }
formatted_requirements = "\n".join([f"- `{field}`: {rule}" for field, rule in field_requirements.items()])

agent_prompt = f"""
You are an assistant specializing in home loan applications. home loan application containing the mandatory fields, \n
{formatted_requirements}. \n
Your goal is to assist users by collecting missing or invalid information from this  mandatory fields and validating the required fields. 
{field_requirements.keys}

Action input should be:
{json.dumps(field_requirements)}

Steps:
1. Validate the user's input for these fields:
   - If a field is missing or invalid, immediately return the corresponding question for that field.
   - For example: If `income` is invalid or missing, return: "What is your annual income? Please provide it in numeric format."

2. Continue collecting and validating fields one at a time until all mandatory fields are valid.

3. Once all fields are valid, return the data in the following JSON format as **final output** of detect_invalid_or_missing_fields tool, as shown in the example:
{json.dumps(formatted_valid_field)}

4. - Only ask a question if the JSON is incomplete or invalid.
**Rules:**
- Only ask a question if the JSON is incomplete or invalid.
- Only ask for one field at a time.
- If the `detect_invalid_or_missing_fields` tool outputs a valid JSON, immediately return that JSON as the final response.
- Do not modify, add context, or rephrase the output from the tool when it is valid.
"""

# Initialize LLM and Agent
llm = OpenAI(model="gpt-4o-mini")
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

def is_valid_json(json_string):
    """
    Verifies if a string is a valid JSON.

    Args:
        json_string (str): The string to validate.

    Returns:
        bool: True if valid JSON, False otherwise.
    """
    try:
        json.loads(json_string)  # Try parsing the string as JSON
        return True
    except json.JSONDecodeError:
        return False
    
def bot_agent_home_loan_recommandation_handle(history, question):
    """
    Handles the home loan recommendation workflow using the agent.
    """
    chat_history = convert_raw_messages_to_chat_messages(history)
    response = asking_key_missing_agent.chat(message=question, chat_history=chat_history)
    logging.info(f"Agent home loan recommendation response: {response.response}")
    if is_valid_json(response.response):
        return home_loan_recommandation(json.loads(response.response))
    return response.response


mock_history = [
    {"role": "system", "content": "You are an assistant for loan recommendations."},
    {"role": "user", "content": "I want to apply for a home loan."},
    {"role": "assistant", "content": "Please provide more information?"},
]

test_cases = [
    # Case 1: User provides valid data
    {
        "history": mock_history,
        "question": "I’m John, and I earn 80000 annually. I need 500000 for a Home purchase. My property is valued at 450000.",
    },
]
print(json.dumps(field_requirements))
history = test_cases[0]["history"]
question = test_cases[0]["question"]

# Execute the function
actual = bot_agent_home_loan_recommandation_handle(history, question)
print(actual)