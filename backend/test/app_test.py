from fastapi.testclient import TestClient
from src.app import app

test_client = TestClient(app)

def test_root():
    """
    Test the root endpoint to ensure the app is running.
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json()[0] ==  "Welcome to Intelligent home loan processing"

# def test_complete_endpoint_sync():
#     """
#     Test the /chat/complete endpoint for synchronous requests.
#     """
    
#     payload = {
#         "bot_id":  "bot_123",
#         "user_id": "user_123",
#         "user_message": "What is the status of my loan?",
#         "sync_request": True
#     }

