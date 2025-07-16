import os
from dotenv import load_dotenv
from app.domain.repositories import MessageSender
from app.domain.entities import Message

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from app.adapters.supabase_adapter import SupabaseAdapter
from datetime import datetime
from app.domain.entities import User

class TelegramAdapter(MessageSender):
    def __init__(self):
        self.supabase = SupabaseAdapter()
        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.handle_start))
        self.app.add_handler(CommandHandler("add", self.handle_add))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_text))

    def send_message(self, message: Message) -> bool:
        # 발송은 크롤링 등 외부 이벤트에서만 사용
        try:
            self.app.bot.send_message(chat_id=message.chat_id, text=message.text)
            return True
        except Exception as e:
            print(f"Telegram send error: {e}")
            return False

    def start_polling(self):
        print("[텔레그램 봇] polling을 시작합니다...")
        self.app.run_polling()

    async def handle_start(self, update, context):
        print(update)
        telegram_id = int(update.effective_chat.id)
        print(f"[수신] /start from {telegram_id}")
        import time
        now_ts = int(time.time())
        user = User(telegram_id=telegram_id, keyword=[], created_at=now_ts)
        self.supabase.register_user(user)
        await context.bot.send_message(chat_id=telegram_id, text="회원 등록이 완료되었습니다.")

    async def handle_add(self, update, context):
        telegram_id = int(update.effective_chat.id)
        print(f"[수신] /add from {telegram_id}, args: {context.args}")
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=telegram_id, text="키워드를 입력하세요. 예시: /add Python")
            return
        keyword = " ".join(context.args)
        self.supabase.add_keyword(telegram_id, keyword)
        await context.bot.send_message(chat_id=telegram_id, text=f"키워드 '{keyword}'가 등록되었습니다.")

    async def handle_text(self, update, context):
        chat_id = str(update.effective_chat.id)
        text = update.message.text
        print(f"[수신] 일반텍스트 from {chat_id}: {text}")
        await context.bot.send_message(chat_id=chat_id, text="명령을 인식하지 못했습니다. /start 또는 /add를 사용하세요.")

    async def handle_text(self, update, context):
        chat_id = str(update.effective_chat.id)
        text = update.message.text
        await context.bot.send_message(chat_id=chat_id, text="명령을 인식하지 못했습니다. /start 또는 /add를 사용하세요.")
