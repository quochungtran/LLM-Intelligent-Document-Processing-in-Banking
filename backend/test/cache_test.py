from src.cache import RedisConversationManager
from src.utils import *

mock_bot_id  = "bot123"
mock_user_id = "user456"
mock_redis_mng = RedisConversationManager(host="localhost", port=6379)

def test_get_conversation_id():
    mock_key        = f"{mock_bot_id}.{mock_user_id}"
    assert mock_key == mock_redis_mng.get_conversation_key(mock_bot_id, mock_user_id)
    _ = mock_redis_mng.get_conversation_id(mock_bot_id, mock_user_id)
    assert mock_redis_mng.is_conversation_key_exist(mock_key) == 1

def test_clear_conversation_id():
    mock_key = mock_redis_mng.get_conversation_key(mock_bot_id, mock_user_id)
    mock_redis_mng.clear_conversation_id(mock_bot_id, mock_user_id)
    assert mock_redis_mng.is_conversation_key_exist(mock_key) == 0