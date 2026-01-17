import discord
from discord import ui

from algomori.data.tag_list import TAG_LIST


class TagButton(ui.Button):
    def __init__(self, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            "관련 문제를 추천받으려면 `!추천 [티어] {tag}` 명령어를 사용하세요.\n"
            "(ex. `!추천 골드 {tag}`)".format(tag=self.label),
        )


class TagButtonView(ui.View):
    def __init__(self, timeout: float = 180):
        super().__init__(timeout=timeout)

        for tag_name in list(TAG_LIST.keys())[:25]:
            self.add_item(TagButton(label=tag_name))
