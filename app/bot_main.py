from app.adapters.telegram_adapter import TelegramAdapter

def main():
    print("[텔레그램 봇] 단독 실행 모드")
    TelegramAdapter().start_polling()

if __name__ == "__main__":
    main()
