import pytest
from sqlalchemy import create_engine
import unittest

from src.database.schemas import ChatConversation
from src.database.models import ChatHistoryManager
from src.database.database import get_db
from src.database.cache import RedisConversationManager
from src.config import Config

# Create engine and session

class TestChatHistoryManagement(unittest.TestCase):
    def setUp(self):
        self._cache = RedisConversationManager(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
        self._db = next(get_db())
        self._dbManager = ChatHistoryManager(self._db, self._cache)
    
    def tearDown(self):
        self._dbManager.clean_chat_conversations()

    def test_load_one_conservation(self):
        """
        Test loading a conversation by conversation_id.
        """
        # Insert test data
        conversation_1 = ChatConversation(
            conversation_id="conv123",
            bot_id="bot123",
            user_id="user456",
            message="Hello!",
            is_request=True,
        )
        self._dbManager.save_conversation(conversation_1)
        fetched_conversation = self._dbManager.load_conversation("conv123")
        
        self.assertEqual(fetched_conversation[0].bot_id,  "bot123")
        self.assertEqual(fetched_conversation[0].message, "Hello!")

    
    def test_load_conservations(self):
        """
        Test loading multiple conversations by conversation_id.
        """
        conversation_1 = ChatConversation(
            conversation_id="conv123",
            bot_id="bot123",
            user_id="user456",
            message="Hello!",
            is_request=True,
        )
        conversation_2 = ChatConversation(
            conversation_id="conv123",
            bot_id="bot123",
            user_id="user456",
            message="Hello! Can I help you ?",
            is_request=False,
        )
        self._dbManager.save_conversations([conversation_1, conversation_2])
        fetched_conversations = self._dbManager.load_conversation("conv123")
        
        self.assertEqual(len(fetched_conversations), 2)
        self.assertEqual(fetched_conversations[0].bot_id,  "bot123")
        self.assertEqual(fetched_conversations[0].message, "Hello!")
        self.assertEqual(fetched_conversations[1].message, "Hello! Can I help you ?")


    def test_update_chat_conversation(self):
        """
        Test creating or updating a chat conversation.
        """
        conversation_1 = ChatConversation(
            conversation_id="conv123",
            bot_id="bot123",
            user_id="user456",
            message="Hello!",
            is_request=True,
        )
        self._dbManager.save_conversation(conversation_1)
        fetched_conversations = self._dbManager.load_conversation("conv123")
        self.assertEqual(fetched_conversations[0].conversation_id, "conv123")

        # update conversation
        # update message but not update bot_id and user_id
        conversation_id = self._dbManager.update_chat_conversation(
            bot_id="bot123",
            user_id="user456",
            message="Hello, bot! I update our message",
            is_request=False,
        )

        fetched_conversations = self._dbManager.load_conversation(conversation_id)
        self.assertEqual(len(fetched_conversations), 1)
        self.assertNotEqual(fetched_conversations[0].conversation_id, "conv123")
        

    def test_convert_conversation_to_openai_messages(self):
        """
        Test converting chat conversations to OpenAI message format.
        """
        conversations = [
            ChatConversation(
                conversation_id="conv123",
                bot_id="bot123",
                user_id="user456",
                message="Hi!",
                is_request=True,
            ),
            ChatConversation(
                conversation_id="conv1234",
                bot_id="bot123",
                user_id="user456",
                message="Hello, how can I help?",
                is_request=False,
            ),
        ]
        result = self._dbManager.convert_conversation_to_openai_messages(conversations)
        expected_result = [
            {"role": "system", "content": "You are an amazing virtual assistant"},
            {"role": "user", "content": "Hi!"},
            {"role": "assistant", "content": "Hello, how can I help?"},
        ]

        self.assertEqual(result, expected_result)


    def test_get_conversation_messages_with_bot(self):
        """
        Test retrieving conversation messages and converting them.
        """
        conversations = [
            ChatConversation(
                conversation_id="conv1234567",
                bot_id="bot12345",
                user_id="user456789",
                message="Hi!",
                is_request=True,
            ),
            ChatConversation(
                conversation_id="conv1234567",
                bot_id="bot12345",
                user_id="user456789",
                message="Hello, how can I help?",
                is_request=False,
            ),
            ChatConversation(
                conversation_id="conv1234567",
                bot_id="bot12345",
                user_id="user456789",
                message="I would like to ask question about home loan application",
                is_request=True,
            ),
        ]
        
        self._dbManager.save_conversations(conversations)
        
        result = self._dbManager.get_conversation_messages("conv1234567")
        expected_result = [
            {"role": "system", "content": "You are an amazing virtual assistant"},
            {"role": "user", "content": "Hi!"},
            {"role": "assistant", "content": "Hello, how can I help?"},
            {"role": "user", "content": "I would like to ask question about home loan application"},
        ]
        self.assertEqual(result, expected_result)
