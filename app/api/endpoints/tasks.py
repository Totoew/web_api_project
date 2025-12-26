from fastapi import APIRouter, BackgroundTasks
from app.tasks.background import manual_fetch_github_events

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/run")
async def run_background_task(
    background_tasks: BackgroundTasks,
):
    """Принудительный запуск фоновой задачи сбора событий с GitHub"""
    # Добавляем задачу в фон
    background_tasks.add_task(manual_fetch_github_events)
    
    return {
        "message": "Фоновая задача запущена вручную",
        "status": "started"
    }