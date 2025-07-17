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
        self.app.add_handler(CommandHandler("help", self.handle_help))
        self.app.add_handler(CommandHandler("a", self.handle_add))
        self.app.add_handler(CommandHandler("l", self.handle_list))
        self.app.add_handler(CommandHandler("d", self.handle_delete))

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
        telegram_id = int(update.effective_chat.id)
        print(f"[수신] /start from {telegram_id}")
        import time
        now_ts = int(time.time())
        user = User(telegram_id=telegram_id, keyword=[], created_at=now_ts)
        self.supabase.register_user(user)
        await context.bot.send_message(chat_id=telegram_id, text="회원 등록이 완료되었습니다.")
        await self.handle_help(update, context)

    async def handle_add(self, update, context):
        telegram_id = int(update.effective_chat.id)
        print(f"[수신] /a from {telegram_id}, args: {context.args}")
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=telegram_id, text="키워드를 입력하세요. 예시: /a Python")
            return
        keyword = " ".join(context.args)
        self.supabase.add_keyword(telegram_id, keyword)
        await context.bot.send_message(chat_id=telegram_id, text=f"키워드 '{keyword}'가 등록되었습니다.")

    async def handle_list(self, update, context):
        telegram_id = int(update.effective_chat.id)
        keywords = self.supabase.get_keywords(telegram_id)
        if not keywords:
            await context.bot.send_message(chat_id=telegram_id, text="등록된 키워드가 없습니다.")
        else:
            await context.bot.send_message(chat_id=telegram_id, text=f"등록된 키워드: {', '.join(keywords)}")

    async def handle_delete(self, update, context):
        telegram_id = int(update.effective_chat.id)
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=telegram_id, text="삭제할 키워드를 입력하세요. 예시: /d Python")
            return
        keyword = " ".join(context.args)
        keywords = self.supabase.get_keywords(telegram_id)
        if keyword not in keywords:
            await context.bot.send_message(chat_id=telegram_id, text=f"'{keyword}'는 등록된 키워드가 아닙니다.")
            return
        keywords.remove(keyword)
        self.supabase.add_keyword(telegram_id, None)  # 키워드 전체 초기화
        for k in keywords:
            self.supabase.add_keyword(telegram_id, k)
        await context.bot.send_message(chat_id=telegram_id, text=f"키워드 '{keyword}'가 삭제되었습니다.")

    async def handle_help(self, update, context):
        help_text = (
            "\u2753 사용 가능한 명령어:\n"
            "/a 키워드 — 키워드 추가 (예: /a Python)\n"
            "/l — 등록된 키워드 조회\n"
            "/d 키워드 — 키워드 삭제 (예: /d Python)\n"
            "/help — 이 도움말 보기\n"
        )
        telegram_id = int(update.effective_chat.id)
        await context.bot.send_message(chat_id=telegram_id, text=help_text)
