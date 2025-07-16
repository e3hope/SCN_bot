from app.domain.repositories import CrawlRepository
from app.domain.entities import CrawlData
from datetime import datetime

class CrawlUseCase:
    def __init__(self, repository: CrawlRepository):
        self.repository = repository

    def execute(self, url: str, title: str, content: str):
        data = CrawlData(
            url=url,
            title=title,
            content=content,
            crawled_at=datetime.utcnow()
        )
        self.repository.save(data)
        return data
