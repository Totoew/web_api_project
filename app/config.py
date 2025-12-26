from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Настройки проекта
    project_name: str = "GitHub Monitor API"
    
    # Настройки БД
    database_url: str = "sqlite+aiosqlite:///./github_events.db"
    
    # Настройки GitHub (можно добавить токен для увеличения лимитов)
    github_base_url: str = "https://api.github.com"
    monitored_repos: List[str] = [
        "fastapi/fastapi",
        "python/cpython",
        "microsoft/vscode"
    ]
    
    # Настройки фоновой задачи
    background_task_interval_seconds: int = 300  # 5 минут
    
    # Настройки NATS
    nats_url: str = "nats://localhost:4222"
    nats_events_channel: str = "github.events"
    nats_commands_channel: str = "github.commands"
    
    class Config:
        env_file = ".env"

settings = Settings()