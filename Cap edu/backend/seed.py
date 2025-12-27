"""
Сид-данные для базы данных QazKids
Инициальные данные для демонстрации
"""

from datetime import datetime
from models import Game, Film, Content
from database import SessionLocal

def seed_games():
    """Добавить примеры игр"""
    db = SessionLocal()
    
    games = [
        Game(
            title="Викторина: Казахские традиции",
            description="Узнайте о казахской культуре, традициях и истории",
            category="quiz",
            difficulty="easy",
            duration_minutes=10,
            image_url="/images/card-kz-1.jpg",
            content='{"questions": [{"q": "Что такое юрта?", "a": "Жилище кочевников"}]}',
            max_score=100
        ),
        Game(
            title="Словарь казахского языка",
            description="Учите новые слова на казахском языке через игру",
            category="word-game",
            difficulty="medium",
            duration_minutes=15,
            image_url="/images/card-kz-2.jpg",
            content='{"words": [{"en": "hello", "kz": "сәлем"}]}',
            max_score=100
        ),
        Game(
            title="Математические пазлы",
            description="Решайте математические задачи в увлекательной форме",
            category="puzzle",
            difficulty="medium",
            duration_minutes=20,
            image_url="/images/card-modern-1.jpg",
            content='{"puzzles": []}',
            max_score=100
        ),
        Game(
            title="Память: Казахская история",
            description="Игра на память с картинками из казахской истории",
            category="memory",
            difficulty="easy",
            duration_minutes=10,
            image_url="/images/card-author.jpg",
            content='{"cards": []}',
            max_score=100
        ),
        Game(
            title="Викторина: География Казахстана",
            description="Тестируйте знания о географии нашей страны",
            category="quiz",
            difficulty="hard",
            duration_minutes=15,
            image_url="/images/card-cinema-1.jpg",
            content='{"questions": []}',
            max_score=100
        ),
    ]
    
    db.add_all(games)
    db.commit()
    print(f"✅ Добавлено {len(games)} игр")
    db.close()


def seed_films():
    """Добавить примеры фильмов"""
    db = SessionLocal()
    
    films = [
        Film(
            title="Мен Қожа Түгімеулі болдым",
            description="Документальный фильм о казахском герое Қожа Түгімеулі",
            duration_minutes=45,
            video_url="https://example.com/video1.mp4",
            thumbnail_url="/images/image-14.png",
            category="history",
            rating=4.8,
            views=150
        ),
        Film(
            title="Казахская кухня: История и традиции",
            description="Учебный фильм о традиционной казахской кухне",
            duration_minutes=30,
            video_url="https://example.com/video2.mp4",
            thumbnail_url="/images/image-69.png",
            category="culture",
            rating=4.6,
            views=120
        ),
        Film(
            title="Великие люди Казахстана",
            description="Серия фильмов о известных казахских писателях и деятелях",
            duration_minutes=60,
            video_url="https://example.com/video3.mp4",
            thumbnail_url="/images/card-cinema-1.jpg",
            category="education",
            rating=4.9,
            views=200
        ),
        Film(
            title="Природа Казахстана",
            description="Красивый фильм о природе и животных Казахстана",
            duration_minutes=50,
            video_url="https://example.com/video4.mp4",
            thumbnail_url="/images/image-14.png",
            category="nature",
            rating=4.7,
            views=180
        ),
    ]
    
    db.add_all(films)
    db.commit()
    print(f"✅ Добавлено {len(films)} фильмов")
    db.close()


def seed_content():
    """Добавить примеры контента (статей)"""
    db = SessionLocal()
    
    content_items = [
        Content(
            title="Как помочь ребёнку учиться эффективнее",
            slug="how-to-help-child-learn",
            body="Практические советы для родителей по поддержке обучения детей...",
            content_type="article",
            author="admin",
            status="published",
            published_at=datetime.utcnow()
        ),
        Content(
            title="Казахский язык: Основные фразы",
            slug="kazakh-language-phrases",
            body="Учебный материал с основными казахскими фразами...",
            content_type="lesson",
            author="teacher",
            status="published",
            published_at=datetime.utcnow()
        ),
        Content(
            title="Безопасность детей в интернете",
            slug="internet-safety-for-kids",
            body="Руководство по безопасному использованию интернета...",
            content_type="guide",
            author="admin",
            status="published",
            published_at=datetime.utcnow()
        ),
        Content(
            title="История Казахского ханства",
            slug="history-of-kazakh-khanate",
            body="Исторический обзор развития Казахского ханства...",
            content_type="article",
            author="teacher",
            status="published",
            published_at=datetime.utcnow()
        ),
    ]
    
    db.add_all(content_items)
    db.commit()
    print(f"✅ Добавлено {len(content_items)} статей")
    db.close()


if __name__ == "__main__":
    print("🌱 Seed data initialization...")
    try:
        seed_games()
        seed_films()
        seed_content()
        print("\n✅ Database seeding completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        
