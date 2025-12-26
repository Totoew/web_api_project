from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from datetime import datetime

from app.models.repo_event import RepoEvent
from app.schemas.repo_event import RepoEventCreate

class EventService:
    @staticmethod
    async def create_event(db: AsyncSession, event_data: RepoEventCreate) -> RepoEvent:
        """Создание нового события в БД"""
        db_event = RepoEvent(**event_data.model_dump())
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return db_event
    
    @staticmethod
    async def get_event(db: AsyncSession, event_id: str) -> Optional[RepoEvent]:
        """Получение события по ID"""
        result = await db.execute(
            select(RepoEvent).where(RepoEvent.id == event_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_events(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[RepoEvent]:
        """Получение всех событий с пагинацией"""
        result = await db.execute(
            select(RepoEvent)
            .order_by(RepoEvent.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def delete_event(db: AsyncSession, event_id: str) -> bool:
        """Удаление события по ID"""
        result = await db.execute(
            delete(RepoEvent).where(RepoEvent.id == event_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def get_events_by_repo(db: AsyncSession, repo_name: str) -> List[RepoEvent]:
        """Получение событий по имени репозитория"""
        result = await db.execute(
            select(RepoEvent)
            .where(RepoEvent.repo_name == repo_name)
            .order_by(RepoEvent.created_at.desc())
        )
        return list(result.scalars().all())