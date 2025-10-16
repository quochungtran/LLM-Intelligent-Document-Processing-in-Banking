from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatConversation:
    id: int
    conversation_id: int
    bot_id: int
    user_id: int 
    message: str
    is_request: bool
    completed: bool
    created_at: datetime
    updated_at: datetime