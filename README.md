# GitHub Monitor API

Асинхронный Backend сервис для мониторинга событий GitHub репозиториев.

## Функциональность

- REST API для управления событиями
- WebSocket для real-time уведомлений
- Фоновая задача для автоматического сбора событий с GitHub
- Интеграция с NATS для публикации/подписки на события
- Асинхронная работа с SQLite БД

## Технологии

- FastAPI
- SQLAlchemy 2.0 + SQLite
- WebSocket
- NATS
- httpx
- Docker + Docker Compose

## Запуск проекта

### Способ 1: Локально (без Docker)

1. Установите зависимости:
```bash
pip install -r requirements.txt