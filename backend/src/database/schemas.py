from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from src.database.database import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)

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

class Profile(Base):
    __tablename__ = 'homeloan_profile'
    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    income = Column(Integer)
    loan_amount = Column(Integer)
    loan_term = Column(Integer)
    loan_to_value_ratio = Column(Float)
    debt_to_income_ratio = Column(Float)
    property_value = Column(Integer)
    home_purpose = Column(String)
