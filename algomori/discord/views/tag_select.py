import discord

from discord import ui

from algomori.data.tag_list import TAG_LIST
from algomori.core.exceptions import ConfigurationError, ProblemNotFoundError, APIError, ParseError
from algomori.discord.embeds import build_problem_embed
from algomori.services.problem_service import ProblemService


class TagSelect(ui.Select):
    def __init__(self, tier: str, problem_service: ProblemService):
        self.tier = tier
        self.problem_service = problem_service

        options = [discord.SelectOption(label="전체(상관없음)", value="__ALL__")]
        options += [
            discord.SelectOption(label=tag, value=tag)
            for tag in list(TAG_LIST.keys())[:24]
        ]

        super().__init__(
            placeholder="원하는 알고리즘 유형을 선택하세요 (선택사항)",
            options=options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        tag = self.values[0]

        try:
            problem = await self.problem_service.get_random_problem(
                self.tier,
                None if tag == "__ALL__" else tag,
            )

            embed = build_problem_embed(
                problem=problem,
                tier=self.tier,
                tag=None if tag == "__ALL__" else tag,
            )

            await interaction.response.edit_message(content=None, embed=embed, view=None)

        except (ConfigurationError, ProblemNotFoundError, APIError, ParseError) as e:
            await interaction.response.edit_message(content=f"오류: {e}", view=None)
        except Exception:
            await interaction.response.edit_message(content="해당 티어와 알고리즘 유형에 맞는 문제가 없습니다.", view=None)


class TagSelectView(ui.View):
    def __init__(self, tier: str, problem_service: ProblemService):
        super().__init__()
        self.add_item(TagSelect(tier=tier, problem_service=problem_service))
