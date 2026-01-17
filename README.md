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
├── 📜 main.py                   # 엔트리포인트 (algomori.app.run 호출)
├── 📜 .env                      # 환경변수 (절대 공개 금지)
├── 📜 requirements.txt          # Python 의존성
├── 📁 algomori/                 # 애플리케이션 패키지
│   ├── 📜 app.py                # 봇 생성/실행, PID/시그널 처리
│   ├── 📁 core/                 # 설정/인터페이스/예외
│   ├── 📁 services/             # solved.ac 연동 + 추천 서비스
│   ├── 📁 domain/               # 도메인 모델
│   │   └── 📁 models/           # Problem 등 데이터 클래스
│   ├── 📁 discord/              # Discord 통합 (cogs, views)
│   │   ├── 📁 cogs/             # 명령어(Commands)
│   │   └── 📁 views/            # UI(Views: 버튼/드롭다운)
│   ├── 📁 data/                 # 정적 데이터(티어/태그)
│   └── 📁 utils/                # 로깅 등 공통 유틸
└── 📁 .github/                  # PR 템플릿 등(선택)
```

### 🧭 디렉토리 역할
- `algomori/app.py`: 봇 실행(엔트리), 의존성 구성, PID/시그널 처리
- `algomori/core/`: 환경설정(`Config`), 인터페이스, 예외 정의
- `algomori/services/`: solved.ac API 호출 및 추천 로직
- `algomori/domain/`: 프로젝트 핵심 데이터 모델(도메인 타입)
- `algomori/discord/`: Discord와 맞닿는 레이어(cogs/views)
- `algomori/data/`: 티어/태그 같은 고정 데이터
- `algomori/utils/`: 로깅 등 공통 유틸리티

### 🔧 기술 스택
- **언어**: Python 3.10+
- **디스코드 라이브러리**: discord.py 2.x
- **API**: solved.ac REST API v3
- **아키텍처 패턴**: 서비스 계층, 의존성 주입, 인터페이스 기반 설계
- **예외 처리**: 계층별 커스텀 예외 시스템

---

## 🛠️ 설치 및 실행

### ✅ 빠른 시작 (Docker/EC2 권장)

전제:
- EC2에 Docker 설치 완료
- 이 저장소의 `Dockerfile`이 있는 위치에서 실행

```bash
# 저장소 클론
git clone https://github.com/byeongkukoh/AlgoMori.git
cd AlgoMori

# (1) 환경변수 파일(.env) 생성 (repo root)
# 필수: DISCORD_BOT_TOKEN
cat > .env <<'EOF'
DISCORD_BOT_TOKEN=your_discord_bot_token_here
# (선택) 서버별 설정 저장 경로
ALGOMORI_GUILD_CONFIG_PATH=/app/runtime/guild_config.json
EOF

# (2) 설정 파일 보관 디렉토리(호스트)
mkdir -p runtime

# (3) 이미지 빌드
docker build -t algomori:latest .

# (4) 컨테이너 실행
# - --env-file 로 .env를 주입
# - runtime/ 볼륨 마운트로 서버별 설정 유지
docker run -d \
  --name algomori \
  --env-file .env \
  -v $(pwd)/runtime:/app/runtime \
  algomori:latest

# 로그 확인
docker logs -f algomori
```

첫 실행 후 Discord 서버에서(원하는 채널에서):
- `!설정` 실행 → 채널/시간(5분 단위) 설정

> `DISCORD_BOT_TOKEN`은 운영 환경에서는 Secret으로 관리하는 것을 권장합니다.

### 🧑‍💻 로컬 개발 (Conda)

```bash
# Conda 가상환경 생성/활성화
conda create -n AlgoMori python=3.10 -y
conda activate AlgoMori

# 의존성 설치
python -m pip install -r requirements.txt

# 로컬 실행
python main.py
```

### 🔐 환경변수

- 필수: `DISCORD_BOT_TOKEN`
- 선택: `ALGOMORI_GUILD_CONFIG_PATH` (기본값: `runtime/guild_config.json`)

로컬 개발 시 repo root에 `.env`를 만들고 다음처럼 입력하세요:

```ini
DISCORD_BOT_TOKEN=your_discord_bot_token_here
ALGOMORI_GUILD_CONFIG_PATH=runtime/guild_config.json
```

### 🤖 Discord 봇 설정
1. Discord Developer Portal에서 애플리케이션 생성
2. Bot 생성 후 토큰 발급
3. Privileged Gateway Intents 활성화
   - `MESSAGE CONTENT INTENT`
   - `SERVER MEMBERS INTENT`
4. OAuth2 URL Generator로 서버에 봇 초대

---

## 📖 사용 가이드

### 🎯 기본 명령어
| 명령어 | 설명 | 예시 |
|--------|------|------|
| `!추천` | 인터랙티브 UI로 문제 추천 | `!추천` |
| `!추천 [티어]` | 특정 난이도 문제 추천 | `!추천 골드` |
| `!추천 [티어] [태그]` | 난이도 + 태그 조건 문제 추천 | `!추천 실버 BFS` |
| `!추천 [티어] [태그] @boj_id` | (선택) 특정 유저가 안 푼 문제 추천(10,000+ solvers) | `!추천 실버 BFS @shiftpsh` |
| `!태그` | 사용 가능한 태그 목록 표시 | `!태그` |
| `!설정` | (관리자) 자동 추천 설정 마법사(채널/시간, 5분 단위) | `!설정` |
| `!설정채널` | (관리자) 자동 추천 채널을 현재 채널로 설정 | `!설정채널` |
| `!설정보기` | 현재 서버 설정 확인 | `!설정보기` |

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
python -c "import asyncio; from algomori.services.problem_service import ProblemService; from algomori.services.api_client import SolvedAcClient; s=ProblemService(SolvedAcClient()); asyncio.run(s.get_random_problem('실버'))"
```

### 🐳 Docker/EC2 운영

운영 배포는 상단의 **"빠른 시작 (Docker/EC2 권장)"** 섹션을 그대로 따릅니다.

- `DISCORD_BOT_TOKEN`은 Secret(환경변수)로 주입
- `runtime/`는 볼륨 마운트로 유지 (서버별 채널/시간 설정 유지)
- 최초 실행 후 Discord에서 `!설정`으로 채널/시간을 설정


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