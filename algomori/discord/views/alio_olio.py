import re

import discord
from discord import ui

from algomori.core.exceptions import APIError, ConfigurationError, ParseError, ProblemNotFoundError
from algomori.discord.embeds import EMBED_COLOR
from algomori.domain.models.problem import Problem
from algomori.services.problem_service import ProblemService


def _parse_handles(text: str) -> list[str]:
    raw = text.strip()
    if not raw:
        return []

    tokens = re.split(r"[\s,]+", raw)
    handles: list[str] = []
    for token in tokens:
        handle = token.strip().lstrip("@").strip()
        if handle:
            handles.append(handle)

    # de-duplicate while preserving order
    seen: set[str] = set()
    result: list[str] = []
    for h in handles:
        if h not in seen:
            seen.add(h)
            result.append(h)

    return result


class _AlioOlioModal(ui.Modal, title="알리오골리오 설정"):
    members = ui.TextInput(
        label="스터디 BOJ 아이디(여러 명)",
        placeholder="예: shiftpsh, tourist, ... (공백/콤마로 구분)",
        required=True,
        style=discord.TextStyle.paragraph,
        max_length=400,
    )

    min_solved = ui.TextInput(
        label="최소 해결 인원 수(선택)",
        placeholder="예: 10000 (빈칸이면 제한없음)",
        required=False,
        max_length=10,
    )

    def __init__(self, *, on_submit_callback):
        super().__init__()
        self._on_submit_callback = on_submit_callback

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self._on_submit_callback(
            interaction,
            members=str(self.members.value or ""),
            min_solved=str(self.min_solved.value or ""),
        )


class AlioOlioView(ui.View):
    """`!추천 알리오골리오` 전용 설정/추천 플로우."""

    def __init__(self, *, problem_service: ProblemService):
        super().__init__(timeout=300)
        self.problem_service = problem_service

        self.member_handles: list[str] = []
        self.min_solved_count: int = 0

    def build_initial_message(self) -> str:
        return (
            "알리오골리오 추천 설정\n"
            "- 스터디 인원의 BOJ 아이디(여러 명)\n"
            "- 최소 해결 인원 수(선택)\n\n"
            "아래 버튼을 눌러 입력하세요."
        )

    def _build_summary(self) -> str:
        members = ", ".join(f"@{h}" for h in self.member_handles) if self.member_handles else "(없음)"
        solved = str(self.min_solved_count) if self.min_solved_count > 0 else "제한없음"

        return (
            "알리오골리오 설정 완료\n"
            f"- 스터디 인원: {members}\n"
            f"- 최소 해결 인원 수: {solved}\n\n"
            "추천을 생성합니다..."
        )

    @ui.button(label="입력하기", style=discord.ButtonStyle.primary)
    async def open_modal(self, interaction: discord.Interaction, button: ui.Button) -> None:
        async def _on_submit(interaction2: discord.Interaction, *, members: str, min_solved: str) -> None:
            handles = _parse_handles(members)
            if not handles:
                await interaction2.response.send_message("스터디 인원 아이디를 1명 이상 입력하세요.", ephemeral=True)
                return

            min_solved_count = 0
            raw_min = min_solved.strip()
            if raw_min:
                if not raw_min.isdigit():
                    await interaction2.response.send_message("최소 해결 인원 수는 숫자만 입력하세요.", ephemeral=True)
                    return
                min_solved_count = int(raw_min)

            self.member_handles = handles
            self.min_solved_count = min_solved_count

            await interaction2.response.edit_message(content=self._build_summary(), view=None)

            # 추천 생성은 follow-up로 진행 (시간이 걸릴 수 있음)
            await self._run_recommendation(interaction2)

        await interaction.response.send_modal(_AlioOlioModal(on_submit_callback=_on_submit))

    async def _run_recommendation(self, interaction: discord.Interaction) -> None:
        try:
            problems = await self._pick_problems()
            embeds = [self._make_embed(problem=p, title=title) for title, p in problems]

            await interaction.followup.send(content="알리오골리오 추천 결과", embeds=embeds)

        except (ConfigurationError, ProblemNotFoundError, APIError, ParseError) as e:
            await interaction.followup.send(f"오류: {e}")
        except Exception as e:
            await interaction.followup.send(f"조건에 맞는 문제를 찾지 못했습니다. ({e})")

    async def _pick_problems(self) -> list[tuple[str, Problem]]:
        used_tags: set[str] = set()

        silver = await self._pick_one("실버", used_tags)
        used_tags.update(silver.tags)

        golds: list[Problem] = []
        for _ in range(3):
            p = await self._pick_one("골드", used_tags)
            used_tags.update(p.tags)
            golds.append(p)

        results: list[tuple[str, Problem]] = [("실버 1문제", silver)]
        results.extend([(f"골드 {idx + 1}/3", p) for idx, p in enumerate(golds)])
        return results

    async def _pick_one(self, tier: str, used_tags: set[str]) -> Problem:
        # 랜덤 추천이라 태그 겹침이 나올 수 있어 반복 시도
        for _ in range(60):
            p = await self.problem_service.get_random_problem(
                tier,
                exclude_solved_by_list=self.member_handles,
                min_solved_count=self.min_solved_count,
            )

            tags = set(p.tags)
            if used_tags.intersection(tags):
                continue

            return p

        raise ProblemNotFoundError("태그가 겹치지 않는 문제를 찾지 못했습니다.")

    def _make_embed(self, *, problem: Problem, title: str) -> discord.Embed:
        return discord.Embed(
            title=title,
            description=f"{problem.title} (난이도: {problem.level})\n{problem.url}",
            color=EMBED_COLOR,
        )
