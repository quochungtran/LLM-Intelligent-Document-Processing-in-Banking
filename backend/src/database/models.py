import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from src.database.database import get_db 
from src.database.cache import cache
from src.database.schemas import ChatConversation  

logger = logging.getLogger(__name__)

class ChatHistoryManager:
    def __init__(self, db, cache):
        self._db = db
        self._cache = cache

    def load_conversation(self, conversation_id: str):
        """
        Return a list of conversations between user and bot given conversation ID.
        """
        return self._db.query(ChatConversation).filter(
            ChatConversation.conversation_id == conversation_id
        ).order_by(ChatConversation.created_at).all()

    async def read_conversation(self, conversation_id: str):
        """
        Asynchronously retrieve a conversation from the database.
        """
        async with self._db() as session:
            result = await session.execute(
                select(ChatConversation).where(ChatConversation.conversation_id == conversation_id)
            )
            db_conversation = result.scalars().first()
            if db_conversation is None:
                raise logger.error("Conversation not found")
            return db_conversation

    def convert_conversation_to_openai_messages(self, user_conversations):
        """
        Convert a list of user conversations to OpenAI API message format.
        """
        conversation_list = [
            {"role": "system", "content": "You are an amazing virtual assistant"}
        ]

        for conversation in user_conversations:
            role = "assistant" if not conversation.is_request else "user"
            content = str(conversation.message)
            conversation_list.append({"role": role, "content": content})

        logger.info(f"Created conversation: {conversation_list}")
        return conversation_list

    def save_conversation(self, conversation: ChatConversation):
        """
        Save a new conversation entry to the database.
        """
        try:
            self._db.add(conversation)
            self._db.commit()
            self._db.refresh(conversation)
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error saving conversation: {e}")
            raise
    
    def save_conversations(self, conversations: list[ChatConversation]):
        """
        Save multiple conversation entries to the database.
        """
        try:
            self._db.add_all(conversations)  # Add multiple objects at once
            self._db.commit()  # Commit the transaction
            for conversation in conversations:
                self._db.refresh(conversation)  # Refresh each conversation object
        except SQLAlchemyError as e:
            self._db.rollback()  # Rollback in case of error
            logger.error(f"Error saving conversations: {e}")
            raise

    def update_chat_conversation(self, bot_id: str, user_id: str, message: str, is_request: bool = True):
        """
        Update chat history by adding a new message to the conversation.
        """
        conversation_id = self._cache.get_conversation_id(bot_id, user_id)

        new_conversation = ChatConversation(
            conversation_id=conversation_id,
            bot_id=bot_id,
            user_id=user_id,
            message=message,
            is_request=is_request,
            completed=not is_request,
        )

        self.save_conversation(new_conversation)
        logger.info(f"Created message for conversation {conversation_id}")

        return conversation_id

    def get_conversation_messages(self, conversation_id):
        """
        Retrieve and format conversation messages.
        """
        user_conversations = self.load_conversation(conversation_id)
        return self.convert_conversation_to_openai_messages(user_conversations)

    def clean_chat_conversations(self):
        """
        Delete all chat conversations from the database.
        """
        try:
            with next(get_db()) as db:
                db.query(ChatConversation).delete()
                db.commit()
                logger.info("All chat conversations have been deleted successfully.")
        except Exception as e:
            logger.error(f"Error cleaning chat conversations: {e}")
