# GitHub Monitor API

Асинхронный Backend сервис для мониторинга событий GitHub репозиториев с использованием FastAPI, WebSocket, NATS и фоновых задач.

## Функциональность

- **REST API** для управления событиями GitHub репозиториев
- **WebSocket** для real-time уведомлений о новых событиях
- **Фоновая задача** для автоматического сбора событий с GitHub API
- **NATS integration** для публикации/подписки на события
- **Асинхронная БД** SQLite с SQLAlchemy 2.0
- **Swagger UI** автоматическая документация API

### Локальный запуск 

#### 1. Установите зависимости
```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте (Linux/Mac)
source venv/bin/activate

# Активируйте (Windows)
venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt
```

2. Запустите NATS сервер

bash
# Используя Docker 
docker run -p 4222:4222 -p 8222:8222 nats:latest

3. Запустите приложение

bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. Откройте в браузере

- Документация API: http://localhost:8000/docs
- ReDoc документация: http://localhost:8000/redoc
- NATS Web UI: http://localhost:8222
- Корневой эндпоинт: http://localhost:8000
