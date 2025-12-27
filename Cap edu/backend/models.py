"""
Модели базы данных QazKids
Модели для хранения всех данных приложения
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    age = Column(Integer)
    role = Column(String, default="student")  # роли: ученик, родитель, учитель, администратор
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    progress = relationship("Progress", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")
    locations = relationship("Location", back_populates="user")


class Game(Base):
    """Модель игры"""
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # категории: викторина, пазл, слова, память
    difficulty = Column(String)  # сложность: легко, средне, сложно
    duration_minutes = Column(Integer, default=10)
    image_url = Column(String)
    content = Column(Text)  # JSON с вопросами/уровнями
    max_score = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    progress = relationship("Progress", back_populates="game")


class Film(Base):
    """Модель фильма"""
    __tablename__ = "films"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer)
    video_url = Column(String)
    thumbnail_url = Column(String)
    category = Column(String)  # категории: история, культура, обучение
    rating = Column(Float, default=0.0)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Progress(Base):
    """Модель прогресса пользователя"""
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    score = Column(Integer, default=0)
    attempts = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    started_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="progress")
    game = relationship("Game", back_populates="progress")


class Achievement(Base):
    """Модель достижения"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    icon_url = Column(String)
    badge_type = Column(String)  # типы: бронза, серебро, золото, платина
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="achievements")


class Location(Base):
    """Модель для хранения GPS данных (родители)"""
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="locations")


class Content(Base):
    """Модель контента (для CMS)"""
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    body = Column(Text)
    content_type = Column(String)  # типы: статья, урок, руководство
    status = Column(String, default="draft")  # статусы: черновик, опубликовано, архив
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)


class Analytics(Base):
    """Модель аналитики"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String)  # события: старт игры, завершение игры, просмотр фильма
    event_data = Column(Text)  # JSON
    timestamp = Column(DateTime, default=datetime.utcnow)
