import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Настройка "Code First" (аналог EF Code First)
# Используем SQLite, как и в C# примере
DATABASE_URL = "sqlite:///content_library_py.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Фабрика сессий (управляет подключениями)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Сущность (Entity)
class ContentItem(Base):
    __tablename__ = "content_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    format = Column(String)  # "Книга", "Видео", "Аудио"
    location = Column(String) # "Локация А", "URL", "Полка 5"

# Создаем таблицы в БД (если их нет)
Base.metadata.create_all(bind=engine)

# 3. Шаблон Repository 
class ContentRepository:
    def __init__(self, session):
        self._session = session

    def get_all(self):
        return self._session.query(ContentItem).all()

    def find(self, query):
        search_query = f"%{query}%"
        return self._session.query(ContentItem).filter(
            (ContentItem.title.like(search_query)) | 
            (ContentItem.format.like(search_query))
        ).all()

    def add(self, item):
        self._session.add(item)

# 4. Шаблон Unit of Work
# В SQLAlchemy сессия (Session) уже сама по себе 
# является реализацией Unit of Work.
# Мы просто делаем удобную "обертку".
class UnitOfWork:
    def __init__(self):
        self.session = SessionLocal()
        self.content_repository = ContentRepository(self.session)

    def save(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def close(self):
        self.session.close()

    # Позволяет использовать 'with UnitOfWork() as uow:'
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()