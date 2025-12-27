from sqlalchemy import String, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid

from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class RepoEvent(Base):
    __tablename__ = "repo_events"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    repo_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_login: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=True)  # Основные данные события
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=True) # Полный ответ от GitHub
    
    def __repr__(self):
        return f"<RepoEvent {self.event_type} for {self.repo_name} at {self.created_at}>"