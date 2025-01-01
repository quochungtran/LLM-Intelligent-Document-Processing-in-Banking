from chat_interface import send_user_request, get_bot_response, get_chat_complete
import unittest

host_chatbot_url = "http://localhost:8082"
bot_id  = "mock_bot2"
user_id = "1002"
text  = "Which states have the highest home loan demand in 2024?"


class TestOpenAIBrain(unittest.TestCase):

    def test_send_user_request(self):
        response = send_user_request(text, bot_id, user_id, host_chatbot_url)
        assert len(response['task_id']) > 0

    def test_get_chat_complete(self):
        # reponse = get_chat_complete(text, bot_id, user_id, host_chatbot_url)
        user_request = send_user_request(text, bot_id, user_id, host_chatbot_url)
        request_id = user_request["task_id"]
        status_code, chat_response = get_bot_response(request_id, host_chatbot_url)
        self.assertEqual(status_code, 200)
        self.assertGreater(len(chat_response['task_result']['content']), 0)
