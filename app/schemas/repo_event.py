from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Базовые схемы
class RepoEventBase(BaseModel):
    repo_name: str
    event_type: str
    actor_login: Optional[str] = None
    created_at: datetime

class RepoEventCreate(RepoEventBase):
    payload: Optional[dict] = None
    raw_data: Optional[dict] = None

class RepoEvent(RepoEventBase):
    id: str
    payload: Optional[dict] = None
    
    class Config:
        from_attributes = True  

class WSEventMessage(BaseModel):
    event_type: str = Field(..., description="Тип события: new_event, updated_event, deleted_event")
    data: RepoEvent