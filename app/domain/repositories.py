from abc import ABC, abstractmethod
from app.domain.entities import CrawlData, Message, User, CrawlingResult
from typing import List, Optional

class CrawlRepository(ABC):
    @abstractmethod
    def save(self, data: CrawlData) -> None:
        pass

    @abstractmethod
    def get_recent(self, limit: int = 10) -> List[CrawlData]:
        pass

class MessageSender(ABC):
    @abstractmethod
    def send_message(self, message: Message) -> bool:
        pass

class UserRepository(ABC):
    @abstractmethod
    def register_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_user(self, telegram_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def add_keyword(self, telegram_id: int, keyword: str) -> None:
        pass

    @abstractmethod
    def get_keywords(self, telegram_id: int) -> List[str]:
        pass

class CrawlingResultRepository(ABC):
    @abstractmethod
    def upsert_results(self, user_id: int, keyword: str, items: List[CrawlingResult]) -> None:
        """유저/키워드별로 최대 5개만 저장, 기존 데이터는 삭제"""
        pass

    @abstractmethod
    def get_results(self, user_id: int, keyword: str, limit: int = 5) -> List[CrawlingResult]:
        """유저/키워드별로 최신순 N개 반환"""
        pass

