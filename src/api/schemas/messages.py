from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: str
    conversation_id: str
    role: str   # 'user' or 'ai'
    content: str
    timestamp: datetime
