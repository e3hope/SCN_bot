from abc import ABC, abstractmethod
from .entities import CrawlData, Message
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
