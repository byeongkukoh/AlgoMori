# Git 브랜치 전략

이 저장소는 `main`(릴리즈)과 `dev`(개발 최신) 2개의 장기 브랜치만 유지하고,
나머지는 **단기 브랜치 + PR**로 운영합니다.

목표:
- `main`은 **릴리즈 스냅샷**만 담는다.
- `dev`는 **항상 최신 개발 버전**을 담는다.
- 모든 변경은 PR로 리뷰/기록한다.

## 1) 장기 브랜치

### `main` (릴리즈용)
- 배포/릴리즈 단위로만 갱신합니다.
- 원칙적으로 직접 작업하지 않고, **`dev`에서 PR로 병합**합니다.
- 릴리즈는 `main`의 커밋에 `vX.Y.Z` 태그를 붙여 고정합니다.

### `dev` (개발 최신)
- 기본 개발 브랜치입니다.
- 기능/버그/리팩터링/문서 변경은 모두 `dev`를 기준으로 진행합니다.
- `main`으로의 릴리즈는 `dev`에서 안정화 후 진행합니다.

## 2) 단기 브랜치(필수)

아래 브랜치는 **작업 단위로 생성 → PR 병합 후 삭제**합니다.

- `feature/<topic>`: 기능 추가/개선
- `fix/<topic>`: 버그 수정
- `docs/<topic>`: 문서 변경(README/CHANGELOG 포함)
- `refactor/<topic>`: 기능 변경 없는 구조 개선
- `chore/<topic>`: 설정/의존성 등
- `wip/<topic>`: 실험/POC (필요 시)

예시:
- `feature/slash-command-recommend`
- `fix/kst-schedule`
- `docs/branching-guide`

## 3) 개발 흐름(기본)

1. `dev` 최신화
   - `git switch dev`
   - `git pull --ff-only origin dev`
2. 단기 브랜치 생성
   - `git switch -c feature/<topic>` (또는 `fix/`, `docs/` 등)
3. 작업 후 커밋
4. 원격 푸시
   - `git push -u origin <branch>`
5. PR 생성 → 리뷰 → `dev`로 merge
6. PR merge 이후 단기 브랜치 삭제

## 4) 릴리즈 흐름 (`dev` → `main`)

릴리즈는 `dev`의 안정화된 상태를 `main`으로 올리는 방식으로 진행합니다.

1. 릴리즈 PR 생성: `dev` → `main`
2. PR merge 후 `main`에서 태그 생성
   - `git tag vX.Y.Z`
   - `git push origin vX.Y.Z`

원칙:
- 릴리즈에 필요한 문서(`CHANGELOG.md`) 갱신도 **`dev`에서 먼저** 반영합니다.
- `main`에만 존재하는 커밋이 생기지 않게(드리프트 방지) 운영합니다.

## 5) Hotfix(긴급 수정)

이미 릴리즈된 버전에 긴급 수정이 필요하면 `main` 기준으로 처리합니다.

1. `main`에서 단기 브랜치 생성
   - `git switch main`
   - `git pull --ff-only origin main`
   - `git switch -c fix/<topic>`
2. PR을 `main`으로 병합
3. `dev`에 역전파
   - `main` → `dev` PR을 생성하여 병합(또는 `dev`에서 `main`을 merge)

## 6) PR 규칙

- `dev`/`main` 직접 푸시는 지양하고 PR로만 병합합니다.
- PR은 가능한 작게 유지합니다(리뷰 가능한 크기).
- PR 설명에는 “왜(why)”를 남깁니다.

## 7) 커밋 메시지 규칙

`README.md`의 접두어 규칙을 그대로 사용합니다.

- `feat:` 새로운 기능 추가
- `fix:` 버그 수정
- `docs:` 문서 수정
- `refactor:` 코드 리팩터링
- `test:` 테스트 코드 추가
