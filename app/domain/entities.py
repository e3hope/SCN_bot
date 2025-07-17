from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CrawlData(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    crawled_at: datetime

class Message(BaseModel):
    chat_id: str
    text: str
    sent_at: Optional[datetime] = None

class User(BaseModel):
    id: Optional[int] = None
    telegram_id: int
    keyword: List[str] = []
    created_at: Optional[datetime] = None
    last_sent_at: Optional[datetime] = None

class UserKeyword(BaseModel):
    id: Optional[int] = None
    chat_id: str
    keyword: str

class CrawlingResult(BaseModel):
    id: Optional[int]
    user_id: int
    keyword: str
    title: str
    link: str
    saved_at: datetime
