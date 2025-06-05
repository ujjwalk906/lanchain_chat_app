# db.py
from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import uuid

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    thread_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    thread_id = Column(String, ForeignKey('conversations.thread_id'), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'ai'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def get_engine(db_url="sqlite:///chat_history.db"):
    return create_engine(db_url)

def get_session(engine):
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

def initialize_database(engine):
    Base.metadata.create_all(engine)
