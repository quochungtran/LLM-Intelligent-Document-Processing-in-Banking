import pytest
import pytest
from llama_index.core.base.llms.types import MessageRole, ChatMessage
from src.agents.agents import convert_raw_messages_to_chat_messages
from src.agents.agents import bot_agent_home_loan_recommandation_handle
import json

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
    {"role": "assistant", "content": "Please provide more information?"},
]

mock_history_1 = [
    {"role": "system", "content": "You are an assistant for loan recommendations."},
    {"role": "user", "content": "I want to apply for a home loan."},
    {"role": "assistant", "content": "Please provide key details ?"},
    {"role": "user", "content":"My name is John, my annual income is 80,000 and my loan amount is 250,000 in 360 months as loan term, "
                               "my property value is 300,000"},
    {"role": "assistant", "content": "What is the purpose of your loan? Please choose one: 'Home purchase', 'Refinance', 'Cash-out refinancing', 'Home improvement', or 'Other purpose'.."}
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
        "question": "Hey, I’m John. I make 80000 a year, and I need take out a loan of 50,0000 for 360 months as loan term, my property value is 450000, and my purpose is Home purchase",
        "expected": "Rejected",
    },
    # Case 2: User provides invalid income
    {
        "history": mock_history,
        "question": "My name is mia, my annual income is abc, and my loan amount is 250,000.",
        "expected": "What is your annual income? Please provide it in numeric format.",
    }
]

def test_bot_agent_home_loan_recommendation_handle():

    history  = test_cases[0]["history"]
    question = test_cases[0]["question"]
    expected = test_cases[0]["expected"]    
    actual = bot_agent_home_loan_recommandation_handle(history, question)
    assert actual == expected

    history  = test_cases[1]["history"]
    question = test_cases[1]["question"]
    expected = test_cases[1]["expected"]
    actual = bot_agent_home_loan_recommandation_handle(history, question)
    assert actual == expected
