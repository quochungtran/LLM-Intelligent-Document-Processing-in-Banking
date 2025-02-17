from src.agents.tools import field_requirements, tools
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
import json

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