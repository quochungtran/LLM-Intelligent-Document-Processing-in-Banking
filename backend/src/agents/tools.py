import logging
from llama_index.core.tools import FunctionTool
logger = logging.getLogger(__name__)


field_requirements = {
    "name": "Must contain alphabetic characters only.",
    "income": "Must be a numeric value (also referred to as annual income).",
    "credit_score": "Must be a numeric value.",
}

# Define mandatory fields
MANDATORY_FIELDS = field_requirements.keys()

# Define field questions
FIELD_QUESTIONS = {
    "name": "What is your name?",
    "income": "What is your annual income? Please provide it in numeric format.",
    "credit_score": "What is your credit score? Please provide it in numeric format.",
}

def validate_input(field_name: str, value: str) -> bool:
    """
    Validates user input based on field type.
    """
    if field_name in ["income", "credit_score"]:
        try:
            int(value)  # Validate as numeric
            return True
        except ValueError:
            return False
    elif field_name == "name":
        return value.isalpha()  # Validate alphabetic name
    return False

def detect_invalid_or_missing_fields(**inputs: dict) -> str:
    """
    Identifies missing or invalid fields in the user input.

    Args:
        inputs (dict): User-provided field data.

    Returns:
        str: Question for the first missing/invalid field, or a JSON if all fields are valid.
    """
    # Iterate through mandatory fields and validate them
    for field in MANDATORY_FIELDS:
        value = inputs.get(field)
        if not value or not validate_input(field, value):
            # Return the question for the first missing/invalid field
            return FIELD_QUESTIONS[field]

    # If all fields are valid, return the validated fields as JSON
    return {"name": inputs["name"], "income": int(inputs["income"]), "credit_score": int(inputs["credit_score"])}


# Convert tools to FunctionTool
detect_missing_field_tool = FunctionTool.from_defaults(fn=detect_invalid_or_missing_fields)

# Select essential tools only
tools = [
    detect_missing_field_tool
]