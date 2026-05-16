# 🔐 Password Analyzer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg" alt="Python 3.12">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-16-blue.svg" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-✔-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
</p>

<p align="center">
  <strong>Современный анализатор стойкости паролей на основе Clean Architecture и DDD</strong>
</p>

---

## 📋 О проекте

**Password Analyzer** — это веб-приложение для анализа стойкости паролей с расчётом энтропии и времени взлома в различных сценариях атак.

Проект построен на принципах:

* 🧱 Clean Architecture
* 🧠 Domain-Driven Design (DDD)
* ⚡ Асинхронной архитектуры FastAPI

---

## ✨ Возможности

* 🎯 Расчёт энтропии пароля (бит)
* ⏱ Оценка времени взлома:

  * Онлайн атака (100 попыток/сек)
  * Онлайн без ограничений (10k/сек)
  * Офлайн bcrypt (1M/сек)
  * GPU MD5 (1T/сек)
* 💪 5 уровней стойкости пароля
* 🎲 Генерация криптостойких паролей
* 📊 Оценка "процентильной силы" пароля
* 🎮 Сценарии для RTX 4090
* 📝 История анализов (PostgreSQL)
* 🎨 UI на Bootstrap 5.3 с тёмной темой
* 🐳 Полная Docker-поддержка

---

## 🚀 Быстрый старт

### 🔧 Docker (рекомендуется)

```bash
git clone https://github.com/your-username/password-analyzer.git
cd password-analyzer

cp .env.example .env

docker compose up --build
```

После запуска:

[http://localhost:8000](http://localhost:8000)

---

### 💻 Локальный запуск

```bash
cd backend

uv sync

uv run alembic upgrade head

uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚙️ Конфигурация (.env)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=password_analyzer
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/password_analyzer

APP_NAME=Password Analyzer
DEBUG=true
SECRET_KEY=your-secret-key-here-change-in-production
```

---

## 🏗️ Архитектура

Presentation Layer (FastAPI, Schemas)
↓
Application Layer (Use Cases, DTO)
↓
Domain Layer (Entities, Value Objects, Rules)
↓
Infrastructure Layer (DB, Repositories)

---

## 📁 Структура проекта

backend/
├── src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
├── alembic/
├── tests/
├── main.py
frontend/
├── index.html
├── style.css
└── app.js

---

## 🔧 Команды

### Docker

docker compose up --build
docker compose up -d
docker compose down
docker compose logs -f

### БД

docker compose exec backend alembic upgrade head
docker compose exec backend alembic revision --autogenerate -m "msg"
docker compose exec backend alembic downgrade -1

## 📡 API

POST /api/v1/analyze
POST /api/v1/generate
GET /api/v1/history

---

## 🧪 Энтропия

Entropy = length × log₂(pool_size)

---

## 🔐 Уровни стойкости

Очень слабый < 28 бит
Слабый 28–36 бит
Средний 36–60 бит
Сильный 60–128 бит
Параноидальный 128+ бит

---

## 🛠️ Технологии

FastAPI, Python 3.12, PostgreSQL 16, SQLAlchemy async, Docker, Bootstrap 5.3, pytest

---

## 🔒 Безопасность

* Нет хранения паролей
* secrets для генерации
* env конфигурация
* CORS
* валидация входных данных

---

## 👨‍💻 Автор

Your Name
GitHub: [https://github.com/your-username](https://github.com/Lissex)

---

## ⚠️ Важно

* После запуска приложение доступно только по адресу:
  👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

* Убедитесь, что используете именно этот URL в браузере.

---

## ⭐ Поддержка

Поставь звезду ⭐
