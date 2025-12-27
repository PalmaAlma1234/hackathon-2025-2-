QazKids — Production Backend

## Overview

QazKids API - полнофункциональный backend для платформы развития детей на казахском языке.

## Features

- ✅ User Authentication (JWT)
- ✅ Game Management
- ✅ Film Library
- ✅ Progress Tracking
- ✅ Achievements System
- ✅ GPS Tracking (Parents)
- ✅ Content Management (CMS)
- ✅ Analytics & Statistics
- ✅ PostgreSQL Database
- ✅ CORS Support

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### Users
- `GET /users/me` - Current user profile
- `PUT /users/me` - Update profile
- `GET /users/{user_id}` - Get user info

### Games
- `GET /games` - List games (filters: category, difficulty)
- `GET /games/{game_id}` - Get game details
- `POST /games` - Create game (admin only)

### Films
- `GET /films` - List films (filters: category)
- `GET /films/{film_id}` - Get film details
- `POST /films` - Create film (admin only)

### Progress
- `POST /progress` - Save game progress
- `GET /progress` - Get user progress
- `GET /progress/{game_id}` - Get progress for specific game

### Achievements
- `GET /achievements` - Get user achievements

### GPS (Parents)
- `POST /locations` - Save GPS coordinates
- `GET /locations` - Get location history

### Content (CMS)
- `GET /content` - List published content
- `GET /content/{slug}` - Get content by slug
- `POST /content` - Create content (admin/teacher)

### Analytics
- `POST /analytics` - Log event
- `GET /analytics/stats` - Get statistics (admin only)

### Health
- `GET /health` - Health check

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=sqlite:///qazkids.db" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env

# Run server
uvicorn fastapi_app:app --reload --port 8000
```

## Docker

```bash
docker build -t qazkids .
docker run -p 8000:8000 qazkids
```

## Models

- **User** - User accounts (students, parents, teachers, admins)
- **Game** - Educational games (quiz, puzzle, word-game, memory)
- **Film** - Educational films/videos
- **Progress** - User game progress tracking
- **Achievement** - User achievements/badges
- **Location** - GPS coordinates (parent monitoring)
- **Content** - CMS articles and guides
- **Analytics** - User events tracking

## Technology Stack

- **Framework:** FastAPI
- **Database:** SQLAlchemy + PostgreSQL/SQLite
- **Authentication:** JWT + bcrypt
- **Validation:** Pydantic
- **API Documentation:** OpenAPI/Swagger

## Security

- Password hashing with bcrypt
- JWT token-based authentication
- CORS enabled for frontend
- SQL injection protection (SQLAlchemy ORM)
- Rate limiting ready (implement with slowapi)

## Development

```powershell
cd "c:\Users\alman\OneDrive\.vscode\Cap edu\backend"
pip install -r requirements.txt
uvicorn fastapi_app:app --reload --port 8000
```

## Version

**v2.0.0** - Production Ready
**Updated:** December 10, 2025
