"""
Pydantic Schemas для валидации данных
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# === СХЕМЫ ПОЛЬЗОВАТЕЛЯ ===
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    age: Optional[int] = None
    role: str = "student"


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# === СХЕМЫ ИГР ===
class GameBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    difficulty: str = "medium"
    duration_minutes: int = 10
    max_score: int = 100


class GameCreate(GameBase):
    image_url: Optional[str] = None
    content: dict  # данные игрового контента в формате JSON


class GameResponse(GameBase):
    id: int
    image_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# === СХЕМЫ ФИЛЬМОВ ===
class FilmBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    category: str


class FilmCreate(FilmBase):
    video_url: str
    thumbnail_url: Optional[str] = None


class FilmResponse(FilmBase):
    id: int
    video_url: str
    thumbnail_url: Optional[str]
    rating: float
    views: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# === СХЕМЫ ПРОГРЕССА ===
class ProgressBase(BaseModel):
    user_id: int
    game_id: int
    score: int


class ProgressCreate(BaseModel):
    game_id: int
    score: int


class ProgressResponse(ProgressBase):
    id: int
    attempts: int
    completed: bool
    completed_at: Optional[datetime]
    started_at: datetime
    
    class Config:
        from_attributes = True


# === СХЕМЫ ДОСТИЖЕНИЙ ===
class AchievementBase(BaseModel):
    title: str
    description: Optional[str] = None
    badge_type: str


class AchievementCreate(AchievementBase):
    icon_url: Optional[str] = None


class AchievementResponse(AchievementBase):
    id: int
    icon_url: Optional[str]
    earned_at: datetime
    
    class Config:
        from_attributes = True


# === СХЕМЫ ЛОКАЦИИ ===
class LocationBase(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float] = None


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# === СХЕМЫ КОНТЕНТА ===
class ContentBase(BaseModel):
    title: str
    slug: str
    body: str
    content_type: str
    author: Optional[str] = None


class ContentCreate(ContentBase):
    pass


class ContentResponse(ContentBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# === СХЕМЫ АУТЕНТИФИКАЦИИ ===
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    user_id: Optional[int] = None


# === СХЕМЫ АНАЛИТИКИ ===
class AnalyticsEvent(BaseModel):
    event_type: str
    event_data: dict


class AnalyticsResponse(AnalyticsEvent):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True
