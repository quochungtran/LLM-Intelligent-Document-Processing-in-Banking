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
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()["response"]), 0)
