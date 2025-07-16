# SCN_bot

SCN_bot은 웹 크롤링을 통해 수집한 정보를 Telegram 봇으로 전달하는 자동화 시스템입니다. FastAPI를 기반으로 하며, Docker로 컨테이너화되어 손쉽게 배포할 수 있습니다. 데이터베이스는 Supabase를 사용합니다.

---

## 주요 기능
- **웹 크롤링**: 다양한 웹사이트에서 정보 수집
- **키워드 검색**: 원하는 URL에서 지정한 키워드가 포함된 본문/제목만 필터링하여 결과 제공
- **Telegram 알림**: 수집된 정보를 Telegram 봇을 통해 실시간 전달
- **Supabase 연동**: 크롤링 데이터 저장 및 관리
- **REST API 제공**: 크롤링 및 메시지 전송을 위한 API 엔드포인트 제공

---

## 프로젝트 구조
```
SCN_bot/
├── app/
│   ├── main.py           # FastAPI 엔트리포인트
│   ├── crawler.py        # 웹 크롤러 모듈
│   ├── telegram_bot.py   # 텔레그램 봇 연동 모듈
│   ├── supabase_client.py# Supabase 연동 모듈
│   ├── models.py         # 데이터 모델 및 스키마
│   └── config.py         # 환경 변수 및 설정 관리
├── requirements.txt      # Python 의존성
├── Dockerfile            # Docker 빌드 파일
├── .env                  # 환경 변수 파일 (Supabase, Telegram Token 등)
└── README.md
```

---

## 환경 변수 (.env 예시)
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TELEGRAM_BOT_TOKEN=your_telegram_token
```

---

## 실행 방법
1. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```
2. **.env 파일 설정**
   - Supabase와 Telegram 정보를 입력
3. **FastAPI 서버 실행**
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Docker로 실행 (선택사항)**
   ```bash
   docker build -t scn_bot .
   docker run --env-file .env -p 8000:8000 scn_bot
   ```

---

## API 사용 예시

### 크롤링 및 키워드 검색 + 텔레그램 알림

- **POST** `/crawl_and_notify/`
- **파라미터**
    - `url`: 크롤링할 대상 페이지 URL
    - `chat_id`: 텔레그램 채팅 ID
    - `keyword`: (선택) 본문/제목에서 찾고 싶은 키워드 (여러 개 가능, 콤마로 구분)
- **동작**
    - 지정한 URL을 크롤링하여, 키워드가 포함된 경우에만 결과를 저장하고 텔레그램으로 알림을 발송합니다.

#### 요청 예시 (JSON)
```json
{
  "url": "https://news.example.com/article/123",
  "chat_id": "123456789",
  "keyword": "AI,Python"
}
```

#### 응답 예시
```json
{
  "result": "success",
  "title": "Python을 활용한 AI 혁신"
}
```

---

## 기술 스택
- **Python 3.11**
- **FastAPI**
- **Docker**
- **Supabase**
- **Telegram Bot API**
- **BeautifulSoup4, httpx** (크롤링)

---

## 아키텍처: 클린 아키텍처 적용

본 프로젝트는 유지보수성과 확장성을 위해 클린 아키텍처(Clean Architecture) 원칙을 따릅니다.

### 계층 구조
- **Domain**: 핵심 비즈니스 로직 및 엔티티, 인터페이스 정의 (`app/domain/`)
- **Usecases**: 유스케이스(비즈니스 규칙) 구현 (`app/usecases/`)
- **Adapters**: 외부 시스템(크롤러, DB, 텔레그램 등)과의 연결 및 구현체 (`app/adapters/`)
- **Interface/API**: FastAPI 엔트리포인트 (`app/main.py`)

### 구조 예시
```
app/
├── domain/                # 엔티티, 리포지토리 인터페이스 등
│   ├── entities.py
│   └── repositories.py
├── usecases/              # 유스케이스(비즈니스 로직)
│   ├── crawl_usecase.py
│   └── notify_usecase.py
├── adapters/              # 외부 시스템 연동(구현체)
│   ├── crawler_adapter.py
│   ├── telegram_adapter.py
│   └── supabase_adapter.py
├── main.py                # FastAPI 엔트리포인트
...
```

### 클린 아키텍처 적용 이유
- **비즈니스 로직과 인프라 분리**: 핵심 로직이 외부 시스템 변화에 영향을 받지 않음
- **테스트 용이성**: 각 계층이 명확히 분리되어 단위 테스트가 쉬움
- **확장성**: 새로운 크롤러, DB, 메시지 시스템 추가가 용이

---

## 파일 설명
- `app/main.py` : FastAPI 서버 및 엔드포인트 정의
- `app/crawler.py` : 웹 크롤러 구현
- `app/telegram_bot.py` : Telegram 메시지 전송 기능
- `app/supabase_client.py` : Supabase 연동 및 데이터 관리
- `app/models.py` : 데이터 모델 및 Pydantic 스키마
- `app/config.py` : 환경 변수 및 설정 관리
- `requirements.txt` : 프로젝트 의존성 목록
- `Dockerfile` : Docker 빌드 설정
- `.env` : 환경 변수 파일

---

## 기여 및 문의
- 이 프로젝트에 기여하고 싶으시거나 문의 사항이 있으시면 이슈를 등록해 주세요.
