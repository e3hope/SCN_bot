from pydantic import BaseModel

class CrawlRequest(BaseModel):
    url: str
    chat_id: str

class CrawlResponse(BaseModel):
    result: str
    title: str
