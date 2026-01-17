import discord

from discord import ui

from algomori.data.tag_list import TAG_LIST
from algomori.discord.views.recommend_filter_select import RecommendFilterSelectView
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
        selected_tag = None if tag == "__ALL__" else tag

        view = RecommendFilterSelectView(
            tier=self.tier,
            tag=selected_tag,
            problem_service=self.problem_service,
        )

        await interaction.response.edit_message(
            content=view.build_initial_message(),
            view=view,
        )


class TagSelectView(ui.View):
    def __init__(self, tier: str, problem_service: ProblemService):
        super().__init__()
        self.add_item(TagSelect(tier=tier, problem_service=problem_service))
