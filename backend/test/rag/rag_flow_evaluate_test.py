from src.rag.rag_flow import bot_rag_answer_message
import unittest

class TestRAGFlow(unittest.TestCase):

    def setUp(self):
        self.history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]
    
    def test_bot_rag_answer_message(self):
        message = "What is the home loan trends in 2024 ?"
        rag_answer = bot_rag_answer_message(self.history, message)

        self.assertIn("trend", rag_answer)

if __name__ == '__main__':
    unittest.main()