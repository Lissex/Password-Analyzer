# 🔐 Password Analyzer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-green.svg" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-blue.svg" />
  <img src="https://img.shields.io/badge/Docker-ready-blue.svg" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
</p>

<p align="center">
  <b>Анализатор стойкости паролей (Clean Architecture + DDD)</b>
</p>

---

## 📋 О проекте

Password Analyzer — сервис для оценки стойкости паролей на основе энтропии и моделирования атак.

---

## ✨ Возможности

- Энтропия пароля (бит)
- Моделирование времени взлома:
  - online 100 попыток/сек
  - online 10k попыток/сек
  - offline bcrypt
  - GPU brute force
- 5 уровней стойкости
- Генерация паролей
- История анализов (PostgreSQL)
- Docker запуск

---

## 🚀 Запуск

### Docker

```bash
git clone https://github.com/your-username/password-analyzer.git
cd password-analyzer

cp .env.example .env

docker compose up --build
```

Открыть:

```
http://127.0.0.1:8000/
```

---

### Локально

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

---

## ⚙️ .env

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=password_analyzer
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/password_analyzer

APP_NAME=Password Analyzer
DEBUG=true
SECRET_KEY=change-me
```

---

## 🧠 Архитектура

```text
Presentation (FastAPI)
        ↓
Application (Use Cases)
        ↓
Domain (Business Logic)
        ↓
Infrastructure (DB, Repos)
```

---

## 📁 Структура

```text
backend/
  src/
    domain/
    application/
    infrastructure/
    presentation/
  alembic/
  tests/
  main.py

frontend/
  index.html
  style.css
  app.js
```

---

## 🔧 Команды

### Docker

```bash
docker compose up --build
docker compose up -d
docker compose down
docker compose logs -f
```

### DB

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend alembic revision --autogenerate -m "msg"
```

---

## 📡 API

```text
POST /api/v1/analyze
POST /api/v1/generate
GET  /api/v1/history
```

---

## 🔐 Стойкость паролей

| Уровень | Биты | Оценка |
|--------|------|--------|
| weak | <28 | мгновенно |
| medium | 28-60 | минуты-дни |
| strong | 60-128 | годы |
| paranoid | 128+ | практически невозможно |

---

## 🛠 Технологии

- FastAPI
- Python 3.12
- PostgreSQL
- SQLAlchemy async
- Docker

---

## ⚠️ Важно

```
Приложение работает только на:
http://127.0.0.1:8000/
```

---

## ⭐ Поддержка

Если полезно — поставь ⭐
