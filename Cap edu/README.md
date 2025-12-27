# 🎓 QazKids - Платформа развития детей Казахстана

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.104-green)
![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)

**QazKids** — инновационная платформа для развития детей, объединяющая игры, образовательные фильмы и интерактивный контент на казахском языке.

---

## 🎯 Наше предложение (UVP)

✨ **100% локализирована на казахский язык**
- Специальный контент для казахских детей
- Культурные ценности интегрированы в обучение
- Единственная платформа с казахским языком для детей

🏫 **Согласование с национальной программой образования**
- ГОСО стандарты
- Поддержка школ
- Сертификация от МОН

🤖 **AI-персонализация обучения**
- GPT интеграция для адаптивных квестов
- Система рекомендаций
- Персональные пути обучения

👨‍👩‍👧‍👦 **Родительский контроль в реальном времени**
- GPS трекинг (безопасность ребёнка)
- Мониторинг прогресса
- Ограничение времени использования

🏆 **Геймификация + Образование**
- Система достижений (bronze, silver, gold)
- Рейтинги и соревнования
- Награды и сертификаты

---

## 📊 Структура проекта

```
Cap edu/
├── desktop.html              # Главная страница
├── styles.css                # Стили
├── play/                      # Раздел "Играть"
│   ├── index.html
│   └── game1-3.html
├── cinema/                    # Раздел "Кино-клуб"
│   ├── index.html
│   └── film1-3.html
├── parents/                   # Раздел "Родителям"
│   ├── index.html
│   └── parents-gps.js
├── images/                    # Изображения и иконки
├── backend/                   # FastAPI Backend
│   ├── fastapi_app.py        # Основное приложение
│   ├── models.py             # Модели БД
│   ├── schemas.py            # Pydantic схемы
│   ├── database.py           # БД конфигурация
│   ├── requirements.txt       # Python зависимости
│   └── README.md             # Backend документация
├── .github/workflows/        # CI/CD pipelines
│   └── ci-cd.yml
├── Dockerfile                # Docker конфигурация
├── docker-compose.yml        # Docker Compose
├── RISK_ANALYSIS.md          # Анализ рисков
└── README.md                 # Этот файл
```

---

## 🚀 Быстрый старт

### Требования
- Python 3.9+
- Docker & Docker Compose (опционально)
- Node.js 18+ (опционально, для фронтенда)

### Локальная установка

1. **Клонировать репозиторий**
```bash
git clone https://github.com/yourusername/qazkids.git
cd qazkids
```

2. **Установить зависимости**
```bash
cd backend
pip install -r requirements.txt
```

3. **Создать .env файл**
```bash
cp .env.example .env
# Отредактировать .env если нужно
```

4. **Запустить сервер**
```bash
uvicorn fastapi_app:app --reload --port 8000
```

5. **Открыть браузер**
```
Frontend: http://localhost:8000
API Docs: http://localhost:8000/docs
```

### Docker Compose (Рекомендуется)

```bash
docker-compose up -d
```

Это запустит:
- 🗄️ PostgreSQL Database
- 💾 Redis Cache
- 🚀 FastAPI Backend (port 8000)
- 🌐 Nginx Frontend (port 80)

---

## 📚 API Документация

### Аутентификация

#### Регистрация
```bash
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "full_name": "John Doe",
  "age": 12,
  "role": "student"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 2592000
}
```

#### Логин
```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

email=john@example.com&password=secure_password

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 2592000
}
```

### Игры

#### Получить список игр
```bash
GET /games?category=quiz&difficulty=easy

Response:
[
  {
    "id": 1,
    "title": "Викторина: Казахские традиции",
    "description": "Узнайте о казахской культуре",
    "category": "quiz",
    "difficulty": "easy",
    "duration_minutes": 10,
    "max_score": 100,
    "created_at": "2025-12-10T10:30:00"
  }
]
```

#### Получить конкретную игру
```bash
GET /games/1

Response:
{
  "id": 1,
  "title": "Викторина: Казахские традиции",
  "description": "Узнайте о казахской культуре",
  "category": "quiz",
  "difficulty": "easy",
  "duration_minutes": 10,
  "max_score": 100,
  "image_url": "https://...",
  "created_at": "2025-12-10T10:30:00"
}
```

### Прогресс

#### Сохранить результат игры
```bash
POST /progress
Authorization: Bearer {token}
Content-Type: application/json

{
  "game_id": 1,
  "score": 85
}

Response:
{
  "id": 1,
  "user_id": 1,
  "game_id": 1,
  "score": 85,
  "attempts": 1,
  "completed": true,
  "completed_at": "2025-12-10T10:45:00",
  "started_at": "2025-12-10T10:30:00"
}
```

#### Получить прогресс пользователя
```bash
GET /progress
Authorization: Bearer {token}

Response:
[
  {
    "id": 1,
    "user_id": 1,
    "game_id": 1,
    "score": 85,
    "attempts": 1,
    "completed": true,
    "completed_at": "2025-12-10T10:45:00"
  }
]
```

### GPS (Родители)

#### Отправить GPS координаты
```bash
POST /locations
Authorization: Bearer {token}
Content-Type: application/json

{
  "latitude": 51.1694,
  "longitude": 71.4491,
  "accuracy": 15.5
}

Response:
{
  "id": 1,
  "latitude": 51.1694,
  "longitude": 71.4491,
  "accuracy": 15.5,
  "timestamp": "2025-12-10T10:30:00"
}
```

---

## 🔐 Безопасность

### Реализованные меры
- ✅ JWT аутентификация
- ✅ Bcrypt хеширование паролей (10 раундов)
- ✅ TLS 1.3 шифрование
- ✅ CORS защита
- ✅ SQL injection защита (SQLAlchemy ORM)
- ✅ XSS защита
- ✅ CSRF tokens

### В разработке
- 🔄 Rate limiting
- 🔄 2FA для администраторов
- 🔄 Сертификация ISO 27001
- 🔄 Регулярные безопасность аудиты

---

## 📈 Стратегия развития

### Phase 1: MVP (✅ Завершена)
- [x] Backend с аутентификацией
- [x] Модели БД
- [x] API endpoints
- [x] Frontend веб-приложение
- [x] GPS функционал
- [x] Система прогресса

### Phase 2: Масштабирование (🔄 In Progress)
- [ ] Мобильные приложения (iOS, Android)
- [ ] Интеграция со школьной системой
- [ ] Партнёрства с 50+ школами
- [ ] Расширение контента

### Phase 3: Монетизация (📅 Q1 2025)
- [ ] Freemium подписка
- [ ] Premium features ($5/месяц)
- [ ] Корпоративные лицензии ($500-2000/школа)
- [ ] Гранты от МОН

### Phase 4: Экспансия (📅 Q2-Q4 2025)
- [ ] Расширение на другие страны Средней Азии
- [ ] Интеграция с YouTube Kids
- [ ] Series A инвестиции

---

## 🧪 Тестирование

### Unit Tests
```bash
pytest backend/tests/ -v
```

### Integration Tests
```bash
pytest backend/tests/integration/ -v --cov=backend
```

### E2E Tests
```bash
npm run test:e2e
```

---

## 🐳 Docker

### Build
```bash
docker build -t qazkids .
```

### Run
```bash
docker run -p 8000:8000 qazkids
```

### Docker Compose
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 📊 Мониторинг

### API Health
```bash
GET /health
```

### Swagger/OpenAPI Docs
```
http://localhost:8000/docs
http://localhost:8000/redoc
```

### Metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

---

## 📝 Лицензия

MIT License - см. [LICENSE](LICENSE) файл

---

## 👥 Команда

- **Almansur** - Founder & Product Manager
- **Нужны:** Backend Lead, Frontend Lead, Content Manager, Marketing Manager

---

## 📞 Контакты

- 📧 Email: info@qazkids.kz
- 📱 Telegram: @qazkids
- 🐦 Twitter: @qazkids_official
- 📘 Instagram: @qazkids_official

---

## 🙏 Поддержка

Если у вас есть вопросы, предложения или баги:
1. Откройте Issue в GitHub
2. Пишите нам в Telegram
3. Email: support@qazkids.kz

---

## 📄 Дополнительная информация

- [Анализ рисков](RISK_ANALYSIS.md)
- [Backend документация](backend/README.md)
- [Бизнес план](BUSINESS_PLAN.md) (coming soon)
- [Roadmap](ROADMAP.md) (coming soon)

---

**Версия:** 2.0.0 (Production Ready)  
**Последнее обновление:** December 10, 2025  
**Статус:** 🟢 Production Ready for Hackathon

---

**Наша миссия:** Сделать качественное образование доступным и увлекательным для каждого ребёнка в Казахстане через инновационные технологии и локальный контент. 🚀
