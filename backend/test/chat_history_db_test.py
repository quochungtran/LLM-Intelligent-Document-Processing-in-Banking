import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import (
    ChatConversation,
    load_conversation,
    update_chat_conversation,
    convert_conversation_to_openai_messages,
    get_conversation_messages,
    save_conversation,
    clean_chat_conversations,
    db
)

from src.database import SQLALCHEMY_DATABASE_URL

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Test the connection
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("Database connection is successful:", result.fetchone())
    except Exception as e:
        print(f"Error connecting to database: {e}")


def test_load_conversation():
    """
    Test loading a conversation by conversation_id.
    """
    # Insert test data
    conversation = ChatConversation(
        conversation_id="conv123",
        bot_id="bot123",
        user_id="user456",
        message="Hello!",
        is_request=True,
    )
    save_conversation(conversation)

    fetched_conversation = load_conversation("conv123")
    assert fetched_conversation[0].bot_id  ==  "bot123"
    assert fetched_conversation[0].message ==  "Hello!"


def test_update_chat_conversation():
    """
    Test creating or updating a chat conversation.
    """
    conversation_id = update_chat_conversation(
        bot_id="bot123",
        user_id="user456",
        message="Hello, bot! I update our message",
        is_request=True,
    )

    fetched_conversation = load_conversation(conversation_id)
    assert fetched_conversation[0].bot_id ==  "bot123"
    assert fetched_conversation[0].message == "Hello, bot! I update our message"

def test_convert_conversation_to_openai_messages():
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
            conversation_id="conv123",
            bot_id="bot123",
            user_id="user456",
            message="Hello, how can I help?",
            is_request=False,
        ),
    ]
    result = convert_conversation_to_openai_messages(conversations)
    expected_result = [
        {"role": "system", "content": "You are an amazing virtual assistant"},
        {"role": "user", "content": "Hi!"},
        {"role": "assistant", "content": "Hello, how can I help?"},
    ]

    assert result == expected_result

def test_get_conversation_messages_without_bot():
    """
    Test retrieving conversation messages and converting them.
    """
    # Insert test data
    conversation = ChatConversation(
        conversation_id="conv12345",
        bot_id="bot1234",
        user_id="user4567",
        message="Hi!",
        is_request=True,
    )

    save_conversation(conversation)
    result = get_conversation_messages("conv12345")
    expected_result = [
        {"content": "You are an amazing virtual assistant", "role": "system"},
        {"content": "Hi!", "role": "user"},
    ]
    assert result == expected_result


def test_get_conversation_messages_with_bot():
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
        )
    ]
    
    for conversation in conversations:
        save_conversation(conversation)
    
    result = get_conversation_messages("conv1234567")
    expected_result = [
        {"role": "system", "content": "You are an amazing virtual assistant"},
        {"role": "user", "content": "Hi!"},
        {"role": "assistant", "content": "Hello, how can I help?"},
    ]
    assert result == expected_result


clean_chat_conversations()
