from datetime import datetime
from app.adapters.supabase_adapter import SupabaseAdapter
from app.adapters.crawler_adapter import CrawlerAdapter
import time

def upsert_crawling_results(supabase: SupabaseAdapter, user_id, keyword, items):
    # 기존 데이터 조회 (최신순)
    rows = supabase.client.table("crawling_result")\
        .select("*")\
        .eq("user_id", user_id)\
        .eq("keyword", keyword)\
        .order("saved_at", desc=True)\
        .execute().data

    # 이미 있는 title+link set
    existing = set((row['title'], row['link']) for row in rows)
    # 새로 들어온 것 중 기존에 없는 것만 추림
    new_items = [item for item in items if (item['title'], item['link']) not in existing]

    # 기존 5개 + 신규 중복 없는 것 합쳐서 최신순 5개만
    all_items = new_items + rows
    all_items = sorted(all_items, key=lambda x: x.get('saved_at', datetime.utcnow()), reverse=True)[:5]

    # 기존 데이터 모두 삭제 후, 새로 5개 insert
    supabase.client.table("crawling_result")\
        .delete()\
        .eq("user_id", user_id)\
        .eq("keyword", keyword)\
        .execute()

    for item in all_items:
        supabase.client.table("crawling_result").insert({
            "user_id": user_id,
            "keyword": keyword,
            "title": item['title'],
            "link": item['link'],
            "saved_at": datetime.utcnow().isoformat()
        }).execute()

def run_crawler_for_all_users():
    supabase = SupabaseAdapter()
    users = supabase.client.table("user").select("id, keyword").execute().data
    for user in users:
        keywords = user.get('keyword', [])
        for keyword in keywords:
            results = CrawlerAdapter.crawl("https://www.fmkorea.com/football_news", keyword)
            upsert_crawling_results(supabase, user['id'], keyword, results)

if __name__ == "__main__":
    run_crawler_for_all_users()
