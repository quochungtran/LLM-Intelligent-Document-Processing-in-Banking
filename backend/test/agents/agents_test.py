import pytest
from src.agents.agents import bot_agent_home_loan_recommandation_handle


import pytest
from llama_index.core.base.llms.types import MessageRole, ChatMessage
from src.agents.agents import convert_raw_messages_to_chat_messages

# Test Cases
test_cases = [
    # Case 1: Basic conversion
    {
        "input": [
            {"role": "system", "content": "You are an assistant for loan recommendations."},
            {"role": "user", "content": "What is the current interest rate?"},
        ],
        "expected": [
            ChatMessage(role=MessageRole.SYSTEM, content="You are an assistant for loan recommendations."),
            ChatMessage(role=MessageRole.USER, content="What is the current interest rate?"),
        ],
    },
    # Case 2: Missing role defaults to USER
    {
        "input": [
            {"content": "Hello! What is the status of my loan?"},
        ],
        "expected": [
            ChatMessage(role=MessageRole.USER, content="Hello! What is the status of my loan?"),
        ],
    },
    # Case 3: Empty input
    {
        "input": [],
        "expected": [],
    },
    # Case 4: Missing content
    {
        "input": [
            {"role": "user"},
        ],
        "expected": [
            ChatMessage(role=MessageRole.USER, content=""),
        ],
    },
]

@pytest.mark.parametrize("test_case", test_cases)
def test_convert_raw_messages_to_chat_messages(test_case):
    input_data = test_case["input"]
    expected_output = test_case["expected"]

    result = convert_raw_messages_to_chat_messages(input_data)

    assert len(result) == len(expected_output), "Mismatch in number of messages"
    for res_msg, exp_msg in zip(result, expected_output):
        assert res_msg.role == exp_msg.role, f"Expected role: {exp_msg.role}, but got: {res_msg.role}"
        assert res_msg.content == exp_msg.content, f"Expected content: {exp_msg.content}, but got: {res_msg.content}"

mock_history = [
    {"role": "system", "content": "You are an assistant for loan recommendations."},
    {"role": "user", "content": "I want to apply for a home loan."},
    {"role": "assistant", "content": "Please provide key details including income, name and credit score ?"}
]

mock_history_1 = [
    {"role": "system", "content": "You are an assistant for loan recommendations."},
    {"role": "user", "content": "I want to apply for a home loan."},
    {"role": "assistant", "content": "Please provide key details including income, name and credit score ?"},
    {"role": "user", "content": "My name is mia, my annual income is abc, and my credit score is 700."},
    {"role": "assistant", "content": "What is your annual income? Please provide it in numeric format."},
]

mock_history_2 = [
    {"role": "system", "content": "You are an assistant for loan recommendations."},
    {"role": "user", "content": "I want to apply for a home loan."},
    {"role": "assistant", "content": "Please provide key details including income, name and credit score ?"},
    {"role": "user", "content": "My name is mia."},
    {"role": "assistant", "content": "What is your annual income? Please provide it in numeric format."},
]

test_cases = [
    # Case 1: User provides valid data
    {
        "history": mock_history,
        "question": "My name is John, my annual income is 60000, and my credit score is 720.",
        "expected": {'name': 'John', 'income': 60000, 'credit_score': 720},
    },
    # Case 2: User provides invalid income
    {
        "history": mock_history,
        "question": "My name is mia, my annual income is abc, and my credit score is 700.",
        "expected": "What is your annual income? Please provide it in numeric format.",
    },
    # Case 3: User provides corrected income 
    {
        "history": mock_history_1,
        "question": "ok, my annual income is 80000.",
        "expected": {'name': 'mia', 'income': 80000, 'credit_score': 700},
    },
    # Case 4: User provides valid income but not format numeric
    {
        "history": mock_history_1,
        "question": "My name is Mia, I have a lot of dogs.",
        "expected": "What is your annual income? Please provide it in numeric format.",
    },
    # Case 5: User provides valid income and need to provide another criteria
    {
        "history": mock_history_2,
        "question": "my annual income is 50000",
        "expected": "What is your credit score? Please provide it in numeric format.",
    }
]

@pytest.mark.parametrize("test_case", test_cases)
def test_bot_agent_home_loan_recommendation_handle(test_case, monkeypatch):
    history = test_case["history"]
    question = test_case["question"]
    expected = test_case["expected"]
    
    # Execute the function
    actual = bot_agent_home_loan_recommandation_handle(history, question)

    assert actual.response == str(expected)
