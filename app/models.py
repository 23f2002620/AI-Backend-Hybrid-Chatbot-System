from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.sql import func


Base = declarative_base()

class EmbeddingsMeta(Base):
    __tablename__ = "embeddings_meta"
    id = Column(Integer, primary_key=True)
    owner_type = Column(String, nullable=False)   # 'faq','message','policy','case'
    owner_id = Column(Integer, nullable=True)     # id in corresponding table if applicable
    vector_id = Column(String, nullable=True)     # for external vector DB (Pinecone) or UUID
    embedding = Column(JSON, nullable=True)       # optional small embedding (for pgvector store as vector type)
    text = Column(Text, nullable=False)           # stored source text (short)
    meta = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    bio = Column(Text)
    gender = Column(String)
    looking_for = Column(String)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer)
    sender_id = Column(Integer)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    reported_user_id = Column(Integer)
    reason = Column(String)
    status = Column(String, default="open")

class TrustScore(Base):
    __tablename__ = "trust_scores"
    user_id = Column(Integer, primary_key=True)
    score = Column(Integer, default=50)

class BotSession(Base):
    __tablename__ = "bot_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    bot_type = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)

class BotMessage(Base):
    __tablename__ = "bot_messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    sender = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class AdminAction(Base):
    __tablename__ = "admin_actions"
    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer)
    action = Column(String)
    target_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
