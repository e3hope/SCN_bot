import os
from supabase import create_client, Client
from app.domain.repositories import CrawlRepository, UserRepository, UserKeywordRepository
from app.domain.entities import CrawlData, User, UserKeyword
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class SupabaseAdapter(CrawlRepository, UserRepository):
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # --- CrawlRepository ---
    def save(self, data: CrawlData) -> None:
        self.client.table("user").insert(data.dict()).execute()

    def get_recent(self, limit: int = 10) -> List[CrawlData]:
        result = self.client.table("user").select("*").order("created_at", desc=True).limit(limit).execute()
        return [CrawlData(**item) for item in result.data]

    # --- UserRepository ---
    def register_user(self, user: User) -> None:
        self.client.table("user").upsert({
            "telegram_id": user.telegram_id,
            "keyword": user.keyword,
            "created_at": user.created_at,
            "last_sent_at": user.last_sent_at
        }).execute()

    def get_user(self, telegram_id: int) -> Optional[User]:
        result = self.client.table("user").select("*").eq("telegram_id", telegram_id).execute()
        if result.data:
            return User(**result.data[0])
        return None

    def add_keyword(self, telegram_id: int, keyword: str) -> None:
        user = self.get_user(telegram_id)
        if user:
            new_keywords = list(set(user.keyword + [keyword]))
            self.client.table("user").update({"keyword": new_keywords}).eq("telegram_id", telegram_id).execute()

    def get_keywords(self, telegram_id: int) -> List[str]:
        user = self.get_user(telegram_id)
        return user.keyword if user else []
