import pytest
from src.task.routing import detect_route
from src.task.routing import llm_handle_message

# Mock data for testing
mock_history = [
    {"role": "system", "content": "You are an amazing virtual assistant"},  
    {"role": "user", "content": "I want to know if my loan is approved."},
    {"role": "assistant", "content": "Please provide your loan ID and key details like income, loan amount, and property value."},
]

test_cases = [
    # Case 1: FAQ Query about general loan trends
    {
        "history": mock_history,
        "message": "What are the current home loan interest rates?",
        "expected": "home_loan_faq",
    },
    # Case 2: Recommendation Query with key loan details
    {
        "history": mock_history,
        "message": "My loan ID is 12345. My income is $80,000, and my loan amount is $250,000. Is my loan approved?",
        "expected": "home_loan_recommandation",
    },
    # Case 3: Irrelevant Query
    {
        "history": mock_history,
        "message": "Can you tell me a joke?",
        "expected": "unknown",
    },
    # Case 4: Edge Case - Empty History
    {
        "history": [],
        "message": "What are the latest loan offers?",
        "expected": "home_loan_faq",
    },
    # Case 5: Ambiguous Query that mentions loans
    {
        "history": mock_history,
        "message": "What can you tell me about home loans?",
        "expected": "home_loan_faq",
    },
    # Case 6: Direct question with incomplete information
    {
        "history": mock_history,
        "message": "My loan ID is 56789. Can you check its status?",
        "expected": "home_loan_recommandation",
    },
]

def test_detect_route(test_case):
    history = test_case["history"]
    message = test_case["message"]
    expected = test_case["expected"]
    
    # Call the function under test
    result = detect_route(history, message)
    
    # Assert that the result matches the expected classification
    assert result == expected, f"Failed for message: {message}, expected: {expected}, got: {result}"

def test_llm_handle_message():
    bot_id   = "bot1"
    user_id  = "user1"
    question = "My income is $80,000, and my loan amount is $250,000. Is my loan approved?"

    expected = {'content': 'What is your name? Please provide it using alphabetic characters only.', 'role': 'assistant'}
    response = llm_handle_message(bot_id=bot_id, user_id=user_id, question=question)
    assert response == expected