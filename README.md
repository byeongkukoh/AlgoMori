# 🧠 AlgoMori

![version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-2.x-blue)
![solved.ac](https://img.shields.io/badge/solved.ac-API-success)
![License](https://img.shields.io/github/license/your_github/AlgoMori)

## 개요

**AlgoMori**는 [solved.ac](https://solved.ac/)의 난이도 기준으로 백준 문제를 난이도별로 랜덤 추천해주는 디스코드 봇입니다.  
매일 지정된 시간에 자동으로 추천 문제를 서버 채널에 전송하고, 사용자가 명령어로 직접 문제를 추천받을 수도 있습니다.

---

## 주요 기능

- 명령어(`!추천 [티어]`)로 브론즈~루비 난이도 백준 문제 랜덤 추천
- 매일 정해진 시간에 자동으로 각 난이도별 추천 문제 전송(Embed)
- solved.ac의 공식/비공식 API를 활용하여 한국어 문제만 필터링
- [Cog] 구조로 명령어/자동화 모듈화 → 유지보수 용이

---

## 디렉토리 구조

```
AlgoMori/
├── main.py # 봇 실행 엔트리포인트
├── config.py # 환경변수 로딩
├── .env # 봇 토큰 및 채널 ID (절대 깃허브에 올리지 마세요)
├── cogs/
│ └── recommender_cog.py # 추천 명령/자동추천 Cog
├── services/
│ └── get_random_problem.py # solved.ac API 연동/로직
├── requirements.txt
└── README.md
```


---

## 설치 및 실행 방법

### 1. 저장소 클론 및 환경 준비

```bash
git clone https://github.com/your_github/AlgoMori.git
cd AlgoMori
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 2. 환경 변수(.env) 파일 작성

`.env` 파일을 프로젝트 루트에 아래 형식으로 생성하세요.

```ini
DISCORD_BOT_TOKEN=여기_디스코드_봇_토큰
DISCORD_CHANNEL_ID=123456789012345678   # 추천 메시지를 전송할 디스코드 채널 ID
```

### 3. 디스코드 개발자 포털 설정

- Bot 토큰 복사: 디스코드 개발자 포털 > 봇 생성 > Token 복사
- Privileged Gateway Intents 설정: MESSAGE CONTENT INTENT 반드시 ON
- 서버에 봇 초대: OAuth2 > URL Generator로 초대 URL 생성 후 본인 서버에 추가

### 4. 봇 실행

```bash
python main.py
```

---

## 사용 방법

### 명령어로 추천

```
!추천 브론즈
!추천 실버
!추천 골드
!추천 플래티넘
!추천 다이아
!추천 루비
```

### 매일 정해진 시간에 자동 추천

- 기본 : KST 기준 오전 8시

---

## 라이선스

- 이 프로젝트는 [MIT 라이선스](https://opensource.org/license/MIT) 하에 배포됩니다.