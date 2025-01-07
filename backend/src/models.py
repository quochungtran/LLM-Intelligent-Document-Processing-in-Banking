import asyncio
import logging
from xml.dom import ValidationErr

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from database import engine

from sqlalchemy.future import select
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

from utils import setup_logging
from database import engine, get_db
from cache import cache
import os

Base = declarative_base()
Base.metadata.create_all(bind=engine)
db =  next(get_db())
setup_logging()
logger = logging.getLogger(__name__)

class ChatConversation(Base):
    __tablename__ = 'chat_conversations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(50), nullable=False, default="")
    bot_id = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False)
    message = Column(String)  # Assuming TextField is equivalent to String in SQLAlchemy
    is_request = Column(Boolean, default=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


def load_conversation(conversation_id: str):
    """
    Return a list of conservations between user and bot given conversation id
    """
    return db.query(ChatConversation).filter(ChatConversation.conversation_id == conversation_id).order_by(ChatConversation.created_at).all()

async def read_conversation(conversation_id: str):
    async with db() as session:
        result = await session.execute(
            select(ChatConversation).where(ChatConversation.conversation_id == conversation_id))
        db_conversation = result.scalars().first()
        if db_conversation is None:
            raise ValidationErr("Conversation not found")
        return db_conversation


def convert_conversation_to_openai_messages(user_conversations):
    conversation_list = [
        {
            "role": "system",
            "content": "You are an amazing virtual assistant"
        }
    ]

    for conversation in user_conversations:
        role = "assistant" if not conversation.is_request else "user"
        content = str(conversation.message)
        conversation_list.append({"role": role, "content": content})

    logging.info(f"Create conversation to {conversation_list}")

    return conversation_list

def save_conversation(conversation: ChatConversation):
    try:
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error saving conversation: {e}")
        raise

def update_chat_conversation(bot_id: str, user_id: str, message: str, is_request: bool = True):
    conversation_id = cache.get_conversation_id(bot_id, user_id)

    new_conversation = ChatConversation(
        conversation_id=conversation_id,
        bot_id=bot_id,
        user_id=user_id,
        message=message,
        is_request=is_request,
        completed=not is_request,
    )

    save_conversation(new_conversation)
    logger.info(f"Create message for conversation {conversation_id}")

    return conversation_id

def get_conversation_messages(conversation_id):
    user_conversations = load_conversation(conversation_id)
    return convert_conversation_to_openai_messages(user_conversations)

def clean_chat_conversations():
    try:
        with next(get_db()) as db:  # Get a database session
            db.query(ChatConversation).delete()  # Delete all rows
            db.commit()  # Commit the transaction
            print("All chat conversations have been deleted successfully.")
    except Exception as e:
        print(f"Error cleaning chat conversations: {e}")