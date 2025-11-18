# Мы импортируем DAL, чтобы использовать его
from dal import UnitOfWork, ContentItem

# Уровень бизнес-логики
class ContentService:
    
    # BLL использует DAL (UnitOfWork)
    def add_content(self, title, format, location):
        # Это пример простой бизнес-логики [cite: 49]
        if not title or not format:
            raise ValueError("Название и формат не могут быть пустыми")
        
        with UnitOfWork() as uow:
            new_item = ContentItem(
                title=title,
                format=format,
                location=location
            )
            uow.content_repository.add(new_item)
            uow.save()

    def get_all_content(self):
        with UnitOfWork() as uow:
            # Мы возвращаем список, чтобы сессия могла закрыться
            return list(uow.content_repository.get_all())

    def search_content(self, query):
        with UnitOfWork() as uow:
            return list(uow.content_repository.find(query))