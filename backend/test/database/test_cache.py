import unittest

from database.cache import RedisConversationManager
from src.utils import *

mock_bot_id  = "bot123"
mock_user_id = "user456"
mock_redis_mng = RedisConversationManager(host="localhost", port=6379)

class TestRedisCache(unittest.TestCase):
    def setUp(self):
        self._cache  = RedisConversationManager(host="localhost", port=6379)
        self._bot_id  = "bot123"
        self._user_id = "user456"

    def tearDown(self):
        self._cache.clear_conversation_id(self._bot_id, self._user_id)

    def test_get_conversation_id(self):
        mock_key = f"{self._bot_id}.{self._user_id}"
        self.assertEqual(self._cache.get_conversation_key(mock_bot_id, mock_user_id), mock_key)
        self.assertFalse(self._cache.is_conversation_key_exist(mock_key))

        # generate new conversation id and add it in cache 
        mock_conversation_id = self._cache.get_conversation_id(mock_bot_id, mock_user_id)
        self.assertTrue(self._cache.is_conversation_key_exist(mock_key))
        self.assertGreater(len(mock_conversation_id), 0)