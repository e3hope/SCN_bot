import os
from dotenv import load_dotenv
from telegram import Bot
from app.domain.repositories import MessageSender
from app.domain.entities import Message

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app.adapters.supabase_adapter import SupabaseAdapter
from datetime import datetime

class TelegramAdapter(MessageSender):
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.supabase = SupabaseAdapter()  # UserRepository, UserKeywordRepository 역할
        self.updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("start", self.register_user))
        dp.add_handler(CommandHandler("add", self.add_keyword))
        dp.add_handler(MessageHandler(Filters.text & (~Filters.command), self.handle_text))

    def send_message(self, message: Message) -> bool:
        try:
            self.bot.send_message(chat_id=message.chat_id, text=message.text)
            return True
        except Exception as e:
            print(f"Telegram send error: {e}")
            return False

    def start_polling(self):
        self.updater.start_polling()

    def register_user(self, update, context):
        telegram_id = int(update.effective_chat.id)
        user = User(telegram_id=telegram_id, keyword=[], created_at=datetime.utcnow())
        self.supabase.register_user(user)
        context.bot.send_message(chat_id=telegram_id, text="회원 등록이 완료되었습니다.")

    def add_keyword(self, update, context):
        telegram_id = int(update.effective_chat.id)
        if len(context.args) == 0:
            context.bot.send_message(chat_id=telegram_id, text="키워드를 입력하세요. 예시: /add Python")
            return
        keyword = " ".join(context.args)
        self.supabase.add_keyword(telegram_id, keyword)
        context.bot.send_message(chat_id=telegram_id, text=f"키워드 '{keyword}'가 등록되었습니다.")

    def handle_text(self, update, context):
        chat_id = str(update.effective_chat.id)
        text = update.message.text
        context.bot.send_message(chat_id=chat_id, text="명령을 인식하지 못했습니다. /start 또는 /add를 사용하세요.")
