from chat_interface import send_user_request, get_bot_response, get_chat_complete

host_chatbot_url = "http://localhost:8082"
bot_id  = "mock_bot2"
user_id = "1002"
text = "Hello, I would like to apply my home loan app?"

def test_send_user_request():
    response = send_user_request(text, bot_id, user_id, host_chatbot_url)
    assert len(response['task_id']) > 0

def test_get_chat_complete():
    # reponse = get_chat_complete(text, bot_id, user_id, host_chatbot_url)
    user_request = send_user_request(text, bot_id, user_id, host_chatbot_url)
    request_id = user_request["task_id"]
    status_code, chat_response = get_bot_response(request_id, host_chatbot_url)
    assert status_code == 200
    assert chat_response['task_status'] == "SUCCESS"
    assert len(chat_response['task_result']['content']) > 0