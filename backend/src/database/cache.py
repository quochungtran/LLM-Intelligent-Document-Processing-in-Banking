import logging
import redis
from utils import generate_request_id
from config import Config

class RedisConversationManager:
    def __init__(self, host="localhost", port=6379, db=0):
        """
        Initialize the ConversationManager with a Redis connection.
        
        :param host: Redis host address (default: "localhost")
        :param port: Redis port (default: 6379)
        :param db: Redis database index (default: 0)
        """
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def is_conversation_key_exist(self, key):
        return self.redis_client.exists(key)

    def is_conversation_key_exist_from(self, bot_id, user_id):
        return self.redis_client.exists(self.get_conversation_key(bot_id, user_id))
        
    def get_conversation_key(self, bot_id, user_id):
        return f"{bot_id}.{user_id}"

    def get_conversation_id(self, bot_id, user_id, ttl_seconds=360):
        key = self.get_conversation_key(bot_id, user_id)
        try:
            if self.is_conversation_key_exist(key):
                self.redis_client.expire(key, ttl_seconds)
                conversation_id = self.redis_client.get(key).decode('utf-8')
                logging.info(f"Fetched existing conversation ID for {key}: {conversation_id}")
                return conversation_id
            else:
                conversation_id = generate_request_id()
                self.redis_client.set(key, conversation_id, ex=ttl_seconds)
                logging.info(f"Created new conversation ID for {key}: {conversation_id}")
                return conversation_id
        except Exception as e:
            logging.exception(f"Get conversation error: {e}")
            return None

    def clear_conversation_id(self, bot_id, user_id):
        key = self.get_conversation_key(bot_id, user_id)
        try:
            self.redis_client.delete(key)
            logging.info(f"Successfully deleted conversation ID for {key}")
            return True
        except Exception as e:
            logging.exception(f"Delete conversation error: {e}")
            return False    
        
cache = RedisConversationManager(host=Config.REDIS_HOST, port=Config.REDIS_PORT)