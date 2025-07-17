from app.adapters.supabase_adapter import SupabaseAdapter
from app.adapters.telegram_adapter import TelegramAdapter
import time

def send_telegram_message(telegram_adapter: TelegramAdapter, chat_id, keyword, items):
    # items: list of dicts with 'title' and 'link'
    if not items:
        return
    text = f"\u2B50 키워드 [{keyword}] 새 소식!\n"
    for item in items:
        text += f"- {item['title']}\n{item['link']}\n"
    telegram_adapter.send_message(type('Msg', (), {'chat_id': chat_id, 'text': text}))

def send_crawling_results_to_users():
    supabase = SupabaseAdapter()
    telegram_adapter = TelegramAdapter()
    users = supabase.client.table("user").select("id, telegram_id, keyword").execute().data
    for user in users:
        chat_id = user.get('telegram_id')
        keywords = user.get('keyword', [])
        for keyword in keywords:
            rows = supabase.client.table("crawling_result")\
                .select("title, link")\
                .eq("user_id", user['id'])\
                .eq("keyword", keyword)\
                .order("saved_at", desc=True)\
                .limit(5)\
                .execute().data
            if rows:
                send_telegram_message(telegram_adapter, chat_id, keyword, rows)

if __name__ == "__main__":
    send_crawling_results_to_users()
