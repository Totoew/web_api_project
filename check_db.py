import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import AsyncSessionLocal
from app.models.repo_event import RepoEvent
from sqlalchemy import select, func

async def check_database():
    print("=" * 50)
    print("Checking database contents...")
    print("=" * 50)
    
    async with AsyncSessionLocal() as session:
        # Подсчитаем общее количество записей
        result = await session.execute(select(func.count()).select_from(RepoEvent))
        total_count = result.scalar()
        print(f"Total records in database: {total_count}")
        
        if total_count == 0:
            print("❌ Database is empty!")
            return
        
        # Посмотрим первые 5 записей
        result = await session.execute(
            select(RepoEvent)
            .order_by(RepoEvent.created_at.desc())
            .limit(5)
        )
        events = result.scalars().all()
        
        print("\nLast 5 events:")
        for event in events:
            print(f"  - ID: {event.id[:8]}...")
            print(f"    Repo: {event.repo_name}")
            print(f"    Type: {event.event_type}")
            print(f"    Actor: {event.actor_login}")
            print(f"    Date: {event.created_at}")
            print()
        
        # Проверим уникальные репозитории
        result = await session.execute(
            select(RepoEvent.repo_name, func.count(RepoEvent.repo_name))
            .group_by(RepoEvent.repo_name)
            .order_by(func.count(RepoEvent.repo_name).desc())
        )
        print("Repositories and event counts:")
        for repo_name, count in result.all():
            print(f"  - {repo_name}: {count} events")
    
    print("=" * 50)
    print("Database check completed!")

if __name__ == "__main__":
    asyncio.run(check_database())