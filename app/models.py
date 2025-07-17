from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CrawlRequest(BaseModel):
    url: str
    chat_id: str

class CrawlResponse(BaseModel):
    result: str
    title: str

class CrawlingResult(BaseModel):
    id: Optional[int]
    user_id: int
    keyword: str
    title: str
    link: str
    saved_at: datetime
