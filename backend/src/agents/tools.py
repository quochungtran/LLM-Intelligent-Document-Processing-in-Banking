import logging
from llama_index.core.tools import FunctionTool
logger = logging.getLogger(__name__)


field_requirements = {
    "name": "Must contain alphabetic characters only.",
    "income": "Must be a numeric value (also referred to as annual income).",
    "loan_amount": "Must be a numeric value",
    "property_value": "Must be a numeric value",
    "loan_term": "Must be a numeric value",
    "loan_purpose":  "Please choose one: 'Home purchase', 'Refinance', "
        "'Cash-out refinancing', 'Home improvement', or 'Other purpose'.",
}

# Define mandatory fields
MANDATORY_FIELDS = field_requirements.keys()

# Define field questions
FIELD_QUESTIONS = {
    "name": "What is your name?",
    "income": "What is your annual income? Please provide it in numeric format.",
    "loan_amount": "What is your loan amount? Please provide it in numeric format.",
    "property_value": "What is your property value? Please provide it in numeric format.",
    "loan_term": "What is your loan term? Must be a numeric value",
    "loan_purpose":  "What is your purpose of home loan application ? Please choose one: 'Home purchase', 'Refinance', "
        "'Cash-out refinancing', 'Home improvement', or 'Other purpose'."
}

def validate_input(field_name: str, value: str) -> bool:
    """
    Validates user input based on field type.
    """
    if field_name in ["income", "loan_term"]:
        try:
            int(value)  # Validate as numeric
            return True
        except ValueError:
            return False
    if field_name in ["loan_amount", "property_value"]:
        try:
            float(value)  # Validate as numeric
            return True
        except ValueError:
            return False
    elif field_name == "name":
        return value.isalpha()  # Validate alphabetic name
    elif field_name == "loan_purpose":
        # Validate against valid loan purposes
        valid_purposes = [
            "Home purchase", "Refinance", "Cash-out refinancing", 
            "Home improvement", "Other purpose"
        ]
        return value in valid_purposes
    return False

def detect_invalid_or_missing_fields(inputs: dict) -> str:
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
        if not value:
            # Return the question for the first missing/invalid field
            return FIELD_QUESTIONS[field]

    # If all fields are valid, return the validated fields as JSON
    return inputs

# Convert tools to FunctionTool
detect_missing_field_tool = FunctionTool.from_defaults(fn=detect_invalid_or_missing_fields)

# Select essential tools only
tools = [
    detect_missing_field_tool
]