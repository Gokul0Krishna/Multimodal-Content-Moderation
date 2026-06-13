from pydantic import BaseModel,HttpUrl
from sqlalchemy import Column, Integer, String, Boolean, DateTime, select
from datetime import datetime
from typing import Optional

class Ingest_input(BaseModel):
    text: str
    img : HttpUrl
    
    
class Api_model(BaseModel):
    """
    SQLAchemy model for storing API keys.
    """
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    key_prefix = Column(String, nullable=False)
    hashed_key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class KeyCreate(BaseModel):
    '''
    schema for creating a new API key.
    '''
    user_id: int
    name: str
    expires_in_days: Optional[int] = None

class KeyResponse(BaseModel):
    name: str
    plain_text_key: str