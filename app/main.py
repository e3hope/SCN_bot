from fastapi import FastAPI, Depends
from app.adapters.supabase_adapter import SupabaseAdapter
from app.adapters.crawler_adapter import CrawlerAdapter
from app.adapters.telegram_adapter import TelegramAdapter
from app.usecases.crawl_usecase import CrawlUseCase
from app.usecases.notify_usecase import NotifyUseCase
from app.models import CrawlRequest, CrawlResponse
import threading
import uvicorn

app = FastAPI()
supabase_adapter = SupabaseAdapter()
crawler_adapter = CrawlerAdapter()
telegram_adapter = TelegramAdapter()
crawl_usecase = CrawlUseCase(supabase_adapter)
notify_usecase = NotifyUseCase(telegram_adapter)

def run_telegram():
    telegram_adapter.start_polling()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

@app.post("/crawl_and_notify/")
def crawl_and_notify(url: str, chat_id: str):
    # 1. 크롤링
    crawl_result = CrawlerAdapter.crawl(url)
    # 2. 저장
    data = crawl_usecase.execute(
        url=crawl_result["url"],
        title=crawl_result["title"],
        content=crawl_result["content"]
    )
    # 3. 텔레그램 알림
    msg = f"[{data.title}] {data.url}\n{data.content[:200]}..."
    success = notify_usecase.execute(chat_id=chat_id, text=msg)
    if not success:
        raise HTTPException(status_code=500, detail="Telegram 전송 실패")
    return {"result": "success", "title": data.title}

@app.get("/recent/")
def get_recent(limit: int = 5):
    data_list = supabase_adapter.get_recent(limit=limit)
    return [d.dict() for d in data_list]
