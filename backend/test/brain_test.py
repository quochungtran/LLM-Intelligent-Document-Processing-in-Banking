from src.brain import openai_chat_complete

def test_openai_chat_complete():
    
    user_prompt = "what is the definition of the loans"
    openai_messages = [
        {"role": "system", "content": "You are a highly intelligent assistant that helps classify customer queries"},
        {"role": "user", "content": user_prompt}
    ]
    
    response = openai_chat_complete(openai_messages)
    assert len(response) > 0