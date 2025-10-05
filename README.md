# 🧠 AlgoMori

![version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-2.x-blue)
![solved.ac](https://img.shields.io/badge/solved.ac-API-success)
![License](https://img.shields.io/github/license/byeongkukoh/AlgoMori)

## 📋 개요

**AlgoMori**는 [solved.ac](https://solved.ac/) API를 활용하여 백준 알고리즘 문제를 난이도별/태그별로 추천해주는 Discord 봇입니다.  
현대적인 아키텍처와 모듈화된 설계로 확장성과 유지보수성을 극대화했습니다.

### ✨ 주요 특징
- **🎯 스마트 추천**: 난이도와 알고리즘 태그 기반 맞춤형 문제 추천
- **⏰ 자동화**: 매일 정해진 시간에 자동 문제 추천
- **🏗️ 모던 아키텍처**: 서비스 계층, 의존성 주입, 인터페이스 기반 설계
- **🛡️ 견고한 예외 처리**: 통합 예외 처리 시스템과 graceful error handling
- **🎨 인터랙티브 UI**: 버튼과 드롭다운을 활용한 직관적인 사용자 인터페이스

---

## 🚀 주요 기능

### 🎲 문제 추천 시스템
- **난이도별 추천**: 브론즈부터 루비까지 solved.ac 난이도 기준
- **태그별 필터링**: DP, DFS, BFS, 그리디 등 25가지 주요 알고리즘 태그
- **인터랙티브 UI**: 버튼 클릭으로 간편한 난이도/태그 선택
- **한국어 문제**: solved.ac API를 통한 한국어 문제만 필터링

### ⚡ 사용 방법
```bash
!추천                    # 인터랙티브 UI로 단계별 선택
!추천 골드               # 골드 난이도 랜덤 문제
!추천 실버 다익스트라     # 실버 + 다익스트라 태그 문제
!태그                   # 사용 가능한 알고리즘 태그 목록
```

### 🕐 자동 추천 시스템
- **매일 오전 8시** (KST 기준) 자동 문제 추천
- **다양한 난이도**: 브론즈, 실버, 골드, 플래티넘 문제 동시 추천
- **Embed 형태**: 깔끔하고 정보가 풍부한 메시지 형태

---

## 🏗️ 아키텍처

### 📁 프로젝트 구조
```
📁 AlgoMori/
├── 📜 main.py                   # 애플리케이션 진입점
├── 📜 .env                      # 환경변수 (절대 공개 금지)
├── 📜 requirements.txt          # Python 의존성
├── 📁 core/                     # 핵심 시스템
│   ├── 📜 config.py            # 환경설정 관리
│   ├── 📜 interface.py         # 서비스 인터페이스
│   └── 📜 exceptions.py        # 커스텀 예외 클래스
├── 📁 services/                 # 비즈니스 로직 계층
│   ├── 📜 problem_service.py   # 문제 추천 서비스
│   ├── 📜 api_client.py        # solved.ac API 클라이언트
│   └── 📜 parsers.py           # 데이터 변환 계층
├── 📁 models/                   # 데이터 모델
│   └── 📜 problem.py           # Problem 데이터클래스
├── 📁 cogs/                     # Discord 명령어 모듈
│   ├── 📜 recommender_cog.py   # 추천 명령어
│   └── 📜 tag_cog.py           # 태그 정보 명령어
├── 📁 views/                    # UI 컴포넌트
│   ├── 📜 tier_select.py       # 난이도 선택 UI
│   └── 📜 tag_select.py        # 태그 선택 UI
├── 📁 data/                     # 정적 데이터
│   ├── 📜 tier_map.py          # 난이도 매핑
│   └── 📜 tag_list.py          # 태그 목록
└── 📁 utils/                    # 유틸리티
    └── 📜 logger.py            # 색상 코드 로깅 시스템
```

### 🔧 기술 스택
- **언어**: Python 3.10+
- **디스코드 라이브러리**: discord.py 2.x
- **API**: solved.ac REST API v3
- **아키텍처 패턴**: 서비스 계층, 의존성 주입, 인터페이스 기반 설계
- **예외 처리**: 계층별 커스텀 예외 시스템

---

## 🛠️ 설치 및 실행

### 1️⃣ 환경 준비
```bash
# 저장소 클론
git clone https://github.com/byeongkukoh/AlgoMori.git
cd AlgoMori

# 가상환경 생성 및 활성화
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2️⃣ 환경변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```ini
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

### 3️⃣ Discord 봇 설정
1. **Discord Developer Portal**에서 새 애플리케이션 생성
2. **Bot** 탭에서 봇 생성 및 토큰 복사
3. **Privileged Gateway Intents**에서 다음 항목 활성화:
   - `MESSAGE CONTENT INTENT`
   - `SERVER MEMBERS INTENT`
4. **OAuth2 > URL Generator**에서 봇 권한 설정:
   - `bot`, `applications.commands`
   - `Send Messages`, `Use Slash Commands`, `Read Message History`

### 4️⃣ 봇 실행
```bash
python main.py
```

성공적으로 실행되면 다음과 같은 로그가 출력됩니다:
```
[INFO] 환경변수 설정을 로드하였습니다.
[INFO] Discord Bot을 시작합니다.
[INFO] AlgoMori으로 로그인되었습니다. (ID: xxxxxxxxxx)
```

---

## 📖 사용 가이드

### 🎯 기본 명령어
| 명령어 | 설명 | 예시 |
|--------|------|------|
| `!추천` | 인터랙티브 UI로 문제 추천 | `!추천` |
| `!추천 [티어]` | 특정 난이도 문제 추천 | `!추천 골드` |
| `!추천 [티어] [태그]` | 난이도 + 태그 조건 문제 추천 | `!추천 실버 BFS` |
| `!태그` | 사용 가능한 태그 목록 표시 | `!태그` |

### 🏅 지원하는 난이도
- **브론즈** (Bronze I~V)
- **실버** (Silver I~V)  
- **골드** (Gold I~V)
- **플래티넘** (Platinum I~V)
- **다이아** (Diamond I~V)
- **루비** (Ruby I~V)

### 🏷️ 주요 알고리즘 태그
- **기초**: DP, DFS, BFS, 그리디, 투 포인터
- **그래프**: 다익스트라, 플로이드-워셜, 크루스칼, 유니온-파인드
- **고급**: 백트래킹, 이분 탐색, 세그먼트 트리, KMP
- **기타**: 스택, 큐, 해시 테이블, 우선순위 큐 등

---

## 🔧 개발자 가이드

### 🏗️ 아키텍처 설계 원칙
- **단일 책임 원칙**: 각 클래스와 모듈은 하나의 책임만 가짐
- **의존성 역전**: 인터페이스에 의존하여 결합도 최소화
- **계층 분리**: API, 서비스, 데이터 계층의 명확한 분리
- **예외 처리**: 계층별 적절한 예외 처리 및 사용자 친화적 메시지

### 🔄 확장 방법
새로운 기능을 추가하려면:

1. **서비스 추가**: `services/` 디렉토리에 새 서비스 클래스 생성
2. **인터페이스 정의**: `core/interface.py`에 추상 클래스 추가
3. **Cog 생성**: `cogs/` 디렉토리에 새 명령어 모듈 추가
4. **예외 처리**: `core/exceptions.py`에 필요한 예외 클래스 추가

### 🧪 테스트
```bash
# 봇 기능 테스트
python main.py

# 개별 모듈 테스트 (예시)
python -c "from services.problem_service import ProblemService; print('OK')"
```

---

## 🤝 기여 방법

1. **Fork** 저장소
2. **Feature 브랜치** 생성 (`git checkout -b feature/amazing-feature`)
3. **변경사항 커밋** (`git commit -m 'Add amazing feature'`)
4. **브랜치에 Push** (`git push origin feature/amazing-feature`)
5. **Pull Request** 생성

### 📋 커밋 메시지 규칙
- `feat:` 새로운 기능 추가
- `fix:` 버그 수정
- `docs:` 문서 수정
- `refactor:` 코드 리팩터링
- `test:` 테스트 코드 추가

---

## 📜 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE) 하에 배포됩니다.

---

## 🙏 감사의 말

- **[solved.ac](https://solved.ac/)**: 훌륭한 API 서비스 제공
- **[discord.py](https://discordpy.readthedocs.io/)**: 강력한 Discord 봇 라이브러리

---

<div align="center">
  <b>📚 Happy Algorithm Learning with AlgoMori! 🚀</b>
</div>