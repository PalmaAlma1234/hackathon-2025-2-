"""
QazKids - FastAPI Backend
Полнофункциональное приложение с аутентификацией, БД, и всеми endpoints
"""

from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import json

from database import get_db, engine
from models import Base, User, Game, Film, Progress, Achievement, Location, Content, Analytics
from schemas import (
    UserCreate, UserResponse, UserUpdate, Token,
    GameCreate, GameResponse, FilmCreate, FilmResponse,
    ProgressCreate, ProgressResponse, AchievementResponse,
    LocationCreate, LocationResponse, ContentCreate, ContentResponse,
    AnalyticsEvent, AnalyticsResponse
)

load_dotenv()

# === CONFIGURATION ===
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

app = FastAPI(
    title="QazKids API",
    description="API для платформы развития детей QazKids",
    version="1.0.0"
)

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === PASSWORD HASHING ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === UTILITY FUNCTIONS ===
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# === STARTUP ===
@app.on_event("startup")
async def startup():
    """Создание таблиц при запуске"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/checked")


# === HEALTH CHECK ===
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "QazKids API is running"}


# === AUTHENTICATION ENDPOINTS ===
@app.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    
    # Проверка существования пользователя
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email или username уже зарегистрирован"
        )
    
    # Создание пользователя
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        age=user_data.age,
        role=user_data.role
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Создание токена
    access_token = create_access_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 30 * 24 * 60 * 60
    }


@app.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Логин пользователя"""
    
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Обновить время последней активности
    user.updated_at = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 30 * 24 * 60 * 60
    }


# === USER ENDPOINTS ===
@app.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """Получить профиль текущего пользователя"""
    return current_user


@app.put("/users/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить профиль пользователя"""
    
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.age:
        current_user.age = user_update.age
    
    db.commit()
    db.refresh(current_user)
    return current_user


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить информацию о пользователе"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# === GAME ENDPOINTS ===
@app.get("/games", response_model=List[GameResponse])
async def get_games(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список игр"""
    query = db.query(Game)
    
    if category:
        query = query.filter(Game.category == category)
    if difficulty:
        query = query.filter(Game.difficulty == difficulty)
    
    return query.all()


@app.get("/games/{game_id}", response_model=GameResponse)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    """Получить информацию об игре"""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.post("/games", response_model=GameResponse)
async def create_game(
    game: GameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новую игру (только для админов)"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create games")
    
    db_game = Game(
        title=game.title,
        description=game.description,
        category=game.category,
        difficulty=game.difficulty,
        duration_minutes=game.duration_minutes,
        image_url=game.image_url,
        content=json.dumps(game.content),
        max_score=game.max_score
    )
    
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


# === FILM ENDPOINTS ===
@app.get("/films", response_model=List[FilmResponse])
async def get_films(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получить список фильмов"""
    query = db.query(Film)
    
    if category:
        query = query.filter(Film.category == category)
    
    return query.offset(skip).limit(limit).all()


@app.get("/films/{film_id}", response_model=FilmResponse)
async def get_film(film_id: int, db: Session = Depends(get_db)):
    """Получить информацию о фильме"""
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Увеличить счётчик просмотров
    film.views += 1
    db.commit()
    
    return film


@app.post("/films", response_model=FilmResponse)
async def create_film(
    film: FilmCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новый фильм (только для админов)"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create films")
    
    db_film = Film(
        title=film.title,
        description=film.description,
        duration_minutes=film.duration_minutes,
        video_url=film.video_url,
        thumbnail_url=film.thumbnail_url,
        category=film.category
    )
    
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


# === PROGRESS ENDPOINTS ===
@app.post("/progress", response_model=ProgressResponse)
async def save_progress(
    progress_data: ProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Сохранить прогресс игры"""
    
    progress = db.query(Progress).filter(
        (Progress.user_id == current_user.id) & 
        (Progress.game_id == progress_data.game_id)
    ).first()
    
    if progress:
        # Обновить существующий прогресс
        progress.score = max(progress.score, progress_data.score)
        progress.attempts += 1
        if progress_data.score > 70:
            progress.completed = True
            progress.completed_at = datetime.utcnow()
    else:
        # Создать новый прогресс
        progress = Progress(
            user_id=current_user.id,
            game_id=progress_data.game_id,
            score=progress_data.score,
            completed=progress_data.score > 70
        )
        if progress_data.score > 70:
            progress.completed_at = datetime.utcnow()
    
    db.add(progress)
    db.commit()
    db.refresh(progress)
    
    return progress


@app.get("/progress", response_model=List[ProgressResponse])
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить прогресс текущего пользователя"""
    return db.query(Progress).filter(Progress.user_id == current_user.id).all()


# === ACHIEVEMENTS ENDPOINTS ===
@app.get("/achievements", response_model=List[AchievementResponse])
async def get_user_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить достижения пользователя"""
    return db.query(Achievement).filter(Achievement.user_id == current_user.id).all()


# === LOCATION ENDPOINTS (GPS) ===
@app.post("/locations", response_model=LocationResponse)
async def save_location(
    location_data: LocationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Сохранить GPS координаты (для родителей)"""
    
    location = Location(
        user_id=current_user.id,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
        accuracy=location_data.accuracy
    )
    
    db.add(location)
    db.commit()
    db.refresh(location)
    
    return location


@app.get("/locations", response_model=List[LocationResponse])
async def get_user_locations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить историю GPS локаций"""
    return db.query(Location).filter(Location.user_id == current_user.id).order_by(
        Location.timestamp.desc()
    ).limit(10).all()


# === CONTENT ENDPOINTS (CMS) ===
@app.get("/content", response_model=List[ContentResponse])
async def get_content(
    content_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получить опубликованный контент"""
    query = db.query(Content).filter(Content.status == "published")
    
    if content_type:
        query = query.filter(Content.content_type == content_type)
    
    return query.order_by(Content.published_at.desc()).offset(skip).limit(limit).all()


@app.get("/content/{slug}", response_model=ContentResponse)
async def get_content_by_slug(slug: str, db: Session = Depends(get_db)):
    """Получить контент по slug"""
    content = db.query(Content).filter(
        (Content.slug == slug) & (Content.status == "published")
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content


@app.post("/content", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новый контент (только для админов и авторов)"""
    
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    content = Content(
        title=content_data.title,
        slug=content_data.slug,
        body=content_data.body,
        content_type=content_data.content_type,
        author=current_user.username,
        status="draft"
    )
    
    db.add(content)
    db.commit()
    db.refresh(content)
    
    return content


# === ANALYTICS ENDPOINTS ===
@app.post("/analytics", response_model=AnalyticsResponse)
async def log_event(
    event: AnalyticsEvent,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Логировать аналитический событие"""
    
    analytics = Analytics(
        user_id=current_user.id,
        event_type=event.event_type,
        event_data=json.dumps(event.event_data)
    )
    
    db.add(analytics)
    db.commit()
    db.refresh(analytics)
    
    return analytics


@app.get("/analytics/stats")
async def get_analytics_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить статистику (только для админов)"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view analytics")
    
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_games = db.query(Game).count()
    total_films = db.query(Film).count()
    completed_games = db.query(Progress).filter(Progress.completed == True).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_games": total_games,
        "total_films": total_films,
        "completed_games": completed_games,
        "timestamp": datetime.utcnow()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
