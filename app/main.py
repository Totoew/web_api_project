from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

from app.config import settings
from app.database import engine, Base
from app.api.routers import routers
from app.websocket import router as ws_router
from app.services.nats_service import nats_client
from app.nats.subscriber import start_nats_subscriber
from app.tasks.background import background_task
from app.services.github_service import github_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan менеджер для управления жизненным циклом приложения"""
    # Startup
    print("=" * 50)
    print("Starting up GitHub Monitor API...")
    print(f"Monitoring repos: {settings.monitored_repos}")
    print(f"Database URL: {settings.database_url}")
    print(f"NATS URL: {settings.nats_url}")
    print("=" * 50)
    
    # Создаем таблицы в БД
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Database tables created successfully")
    except Exception as e:
        print(f"Database error: {e}")
    

    await nats_client.connect()
    print(f"✅ NATS connected: {nats_client.is_connected}")
    
    # Запускаем подписчика NATS
    try:
        await start_nats_subscriber()
        print("✅ NATS subscriber started")
    except Exception as e:
        print(f"❌ NATS subscriber error: {e}")
    
    # Запускаем фоновую задачу
    task = asyncio.create_task(background_task())
    print("✅ Background task started")
    
    yield
    
    # Shutdown
    print("\n" + "=" * 50)
    print("Shutting down...")
    
    # Отменяем фоновую задачу
    task.cancel()
    try:
        await task
        print("✅ Background task stopped gracefully")
    except asyncio.CancelledError:
        print("⚠️  Background task cancelled")
    except Exception as e:
        print(f"❌ Error stopping background task: {e}")
    
    # Закрываем соединение с NATS
    await nats_client.close()
    print("✅ NATS connection closed")
    
    # Закрываем HTTP клиент
    await github_service.close()
    print("✅ GitHub service closed")
    print("=" * 50)

# Создаем приложение FastAPI
app = FastAPI(
    title=settings.project_name,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API роутеры
for router in routers:
    app.include_router(router)

# Подключаем WebSocket роутер
app.include_router(ws_router)

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "GitHub Monitor API",
        "docs": "/docs",
        "websocket": "/ws/events",
        "monitored_repos": settings.monitored_repos
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "nats_connected": nats_client.is_connected
    }