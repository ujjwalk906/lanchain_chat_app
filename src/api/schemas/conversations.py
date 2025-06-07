from pydantic import BaseModel
from datetime import datetime


class ConversationCreate(BaseModel):
    name: str

class ConversationOut(BaseModel):
    id: str         # or thread_id
    name: str
    created_at: datetime
    last_message: str | None = None   # optional, for previews
    last_updated: datetime | None = None  # optional

class ConversationUpdate(BaseModel):
    name: str

class DeleteResponse(BaseModel):
    success: bool
    detail: str | None = None