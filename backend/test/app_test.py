from fastapi.testclient import TestClient
from src.app import app
from src.app import CompleteRequest
import json
import unittest

test_client = TestClient(app)

class TestApp(unittest.TestCase):

    def test_root(self):
        """
        Test the root endpoint to ensure the app is running.
        """
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.json()[0] == "Welcome to Intelligent home loan processing"

    def test_chat_complete_endpoint_sync(self):
        """
        Test the /chat/complete endpoint for synchronous requests.
        """
        payload = {
            "bot_id": "best_homeloan_bot",
            "user_id": "Hung",
            "user_message": "Which states have the highest home loan demand in 2024?",
            "sync_request": True
        }
        response = test_client.post("/chat/complete", json=payload)

        # bot_answer = (
        #     "To assist you with your home loan application, "
        #     "I need to collect some information from you. Let's start with your name. "
        #     "What is your name? Please provide it using alphabetic characters only."
        # )

        # expected = {'content': bot_answer, "role": 'assistant'}
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()["response"]), 0)

# def test_chat_complete_task_flow():
#     """
#     Test the full task lifecycle:
#     - Create a task
#     - Poll its status
#     - Verify the final result
#     """
#     payload = {
#         "bot_id": "best_homeloan_bot",
#         "user_id": "Hung",
#         "user_message": "Hello, I want to know if my home loan application is approved",
#         "sync_request": False
#     }

#     response = test_client.post("/chat/complete", json=payload)
#     assert response.status_code == 200

#     # post_data = response.json()
#     # task_id = post_data["task_id"]

#     # assert len(task_id) > 0
