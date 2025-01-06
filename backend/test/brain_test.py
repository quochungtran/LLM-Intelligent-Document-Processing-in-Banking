from src.brain import detect_route, gen_doc_prompt, openai_chat_complete, detect_user_intent, generate_conversation_text, detect_collection
import unittest


class TestOpenAIBrain(unittest.TestCase):

    def setUp(self):
        self.history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]

    def test_generate_conversation_text(self):
        expected_output = "user: Hello\nassistant: Hi there! How can I help you today?\n"
        result = generate_conversation_text(self.history)
        self.assertEqual(result, expected_output)

    def test_openai_chat_complete(self):   
        user_prompt = "what is the definition of the loans" 
        openai_messages = [
            {"role": "system", "content": "You are a highly intelligent assistant that helps classify customer queries"},
            {"role": "user", "content": user_prompt}
        ]
        
        response = openai_chat_complete(openai_messages)
        self.assertGreater(len(response), 0)

    def test_detect_user_intent(self):
        message = "What can you tell me about Python?"
        result = detect_user_intent(self.history, message)
        self.assertIn("Python", result)

    def test_detect_collection(self):
        message = "Which states have the highest home loan demand in 2024?"
        result = detect_collection(self.history, message)
        self.assertIn('market_trends', result)

    def test_detect_route(self):
        route_message = "Can you explain about home loan approval?"
        result = detect_route(self.history, route_message)
        self.assertEqual(result, "home_loan_faq")

        route_message = "I would ask about a home loan applications if it can be approved or not"
        result = detect_route(self.history, route_message)
        self.assertEqual(result, "home_loan_recommandation")

    def test_gen_doc_prompt(self):
        docs = [
            {"content": "This is the first document."},
            {"content": "This is the second document."}
        ]
        expected_output = "Document: \n + Content: This is the first document. \nContent: This is the second document. \n"

        result = gen_doc_prompt(docs)
        self.assertEqual(result, expected_output)
if __name__ == '__main__':
    unittest.main()