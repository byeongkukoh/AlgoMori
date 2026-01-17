import discord
from discord import ui

from algomori.core.exceptions import ConfigurationError, ProblemNotFoundError, APIError, ParseError
from algomori.discord.embeds import build_problem_embed
from algomori.services.problem_service import ProblemService


_SOLVED_COUNT_OPTIONS: list[tuple[str, int]] = [
    ("제한없음", 0),
    ("2,000명 이상", 2000),
    ("4,000명 이상", 4000),
    ("6,000명 이상", 6000),
    ("8,000명 이상", 8000),
    ("10,000명 이상", 10000),
]


class _UserIdModal(ui.Modal, title="BOJ 아이디(선택)"):
    user_id = ui.TextInput(
        label="BOJ 아이디",
        placeholder="빈칸이면 무시(필터 해제)",
        required=False,
        max_length=32,
    )

    def __init__(self, *, on_submit_callback):
        super().__init__()
        self._on_submit_callback = on_submit_callback

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self._on_submit_callback(interaction, str(self.user_id.value or ""))


class SolvedCountSelect(ui.Select):
    def __init__(self, *, view: "RecommendFilterSelectView", initial_value: int):
        self._view = view

        options = [
            discord.SelectOption(
                label=label,
                value=str(value),
                default=(value == initial_value),
            )
            for label, value in _SOLVED_COUNT_OPTIONS
        ]

        super().__init__(
            placeholder="푼 사람 수 필터(선택)",
            options=options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self._view.min_solved_count = int(self.values[0])
        await self._view.render(interaction)


class RecommendFilterSelectView(ui.View):
    def __init__(
        self,
        *,
        tier: str,
        tag: str | None,
        problem_service: ProblemService,
    ):
        super().__init__(timeout=300)

        self.tier = tier
        self.tag = tag
        self.problem_service = problem_service

        self.exclude_solved_by: str | None = None
        self.min_solved_count: int = 0

        self._solved_count_select = SolvedCountSelect(view=self, initial_value=self.min_solved_count)
        self.add_item(self._solved_count_select)

        self._sync_controls()

    def build_initial_message(self) -> str:
        return self._build_content()

    def _build_content(self) -> str:
        tag_text = self.tag if self.tag else "(전체)"
        user_text = f"@{self.exclude_solved_by}" if self.exclude_solved_by else "(미사용)"

        solved_text = None
        for label, value in _SOLVED_COUNT_OPTIONS:
            if value == self.min_solved_count:
                solved_text = label
                break

        solved_text = solved_text or str(self.min_solved_count)

        return (
            f"선택한 티어: {self.tier}\n"
            f"선택한 태그: {tag_text}\n\n"
            "추가 필터(선택사항)를 설정하세요.\n"
            f"- 유저 미해결 필터: {user_text}\n"
            f"- 푼 사람 수: {solved_text}\n"
        )

    def _sync_controls(self) -> None:
        # Always enabled for now (single-step view)
        pass

    async def render(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(content=self._build_content(), view=self)

    @ui.button(label="BOJ 아이디 입력", style=discord.ButtonStyle.secondary)
    async def set_user_id(self, interaction: discord.Interaction, button: ui.Button) -> None:
        async def _on_submit(interaction2: discord.Interaction, value: str) -> None:
            handle = value.strip().lstrip("@").strip()
            self.exclude_solved_by = handle or None
            await interaction2.response.edit_message(content=self._build_content(), view=self)

        await interaction.response.send_modal(_UserIdModal(on_submit_callback=_on_submit))

    @ui.button(label="추천 받기", style=discord.ButtonStyle.primary)
    async def recommend(self, interaction: discord.Interaction, button: ui.Button) -> None:
        try:
            problem = await self.problem_service.get_random_problem(
                self.tier,
                self.tag,
                exclude_solved_by=self.exclude_solved_by,
                min_solved_count=self.min_solved_count,
            )

            embed = build_problem_embed(
                problem=problem,
                tier=self.tier,
                tag=self.tag,
            )

            await interaction.response.edit_message(content=None, embed=embed, view=None)

        except (ConfigurationError, ProblemNotFoundError, APIError, ParseError) as e:
            await interaction.response.edit_message(content=f"오류: {e}", view=None)
        except Exception:
            await interaction.response.edit_message(content="조건에 맞는 문제를 찾을 수 없습니다.", view=None)

    @ui.button(label="취소", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button) -> None:
        self.stop()
        await interaction.response.edit_message(content="취소했습니다.", view=None)

    async def on_timeout(self) -> None:
        for child in self.children:
            if isinstance(child, (ui.Button, ui.Select)):
                child.disabled = True
