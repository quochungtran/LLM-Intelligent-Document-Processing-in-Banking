from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.base.llms.types import MessageRole, ChatMessage
import logging
import sys
import os
from brain import collect_homeloan_information
from src.agents.tools import detect_invalid_or_missing_fields, field_requirements, tools
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

field_requirements_samples = {
    "name":   "alphabetic or null",
    "income": "numeric or null",
    "loan_amount": "numeric or null",
    "property_value": "numeric or null",
    "loan_term": "numeric or null",
    "loan_purpose":  "choose one in the list ['Home purchase', 'Refinance', "
        "'Cash-out refinancing', 'Home improvement', or 'Other purpose'].",
}

formatted_requirements = "\n".join([f"- `{field}`: {rule}" for field, rule in field_requirements.items()])

agent_prompt = f"""
You are an assistant specializing in home loan applications containing the mandatory fields, \n
{formatted_requirements}. \n
Your goal is to assist users by collecting missing or invalid information from this  mandatory fields and validating the required fields. 
{field_requirements.keys}

Steps:
1. Given the following the user's latest message and chat history, detecting and gathering all information (valid or missing)
    of a home loan application and assign to the json output following the format:
    {json.dumps(field_requirements_samples)}

2. Validate the user's input for these fields:
   - If a field is missing or invalid, immediately return the corresponding question for that field.
   - For example: If `income` is invalid or missing, return: "What is your annual income? Please provide it in numeric format."

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

def bot_agent_home_loan_recommandation_handle(history, message):
    """
    Handles the home loan recommendation workflow using the agent.
    """
    chat_history = convert_raw_messages_to_chat_messages(history)
    # response = asking_key_missing_agent.chat(message=message, chat_history=chat_history)
    homeloan_application = collect_homeloan_information(chat_history, message)
    response             = detect_invalid_or_missing_fields(json.loads(homeloan_application))
    logging.info(f"Agent home loan recommendation response: {response}")
    if isinstance(response, dict):
        return home_loan_recommandation(response)
    return response

mock_history = [
    {"role": "system", "content": "You are an assistant for loan recommendations."},
    {"role": "user", "content": "I want to apply for a loan."},
    {"role": "assistant", "content": "Please provide more information?"},
]

test_cases = [
    {
        "history": mock_history,
        "question": "I’m John, and I earn 80000 annually. I need 500000. My property is valued at 450000. and I need a loan for 360 months",
    },
]
history = test_cases[0]["history"]
question = test_cases[0]["question"]

# Execute the function
actual = bot_agent_home_loan_recommandation_handle(history, question)
print(actual)