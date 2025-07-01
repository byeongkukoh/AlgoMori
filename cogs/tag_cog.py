import discord

from data.tag_list import TAG_LIST
from data.tier_map import TIER_MAP, TIERS

from discord import ui
from discord.ext import commands, tasks

class TagButton(ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"관련 문제를 추천받으려면 `!추천 [티어] {self.label}` 명령어를 사용하세요.\n(ex. `!추천 골드 {self.label}`)",
        )


class TagButtonView(ui.View):
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)

        for i, tag_name in enumerate(TAG_LIST.keys()):
            if i >= 25:
                break
            self.add_item(TagButton(label=tag_name))


class TagCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='태그')
    async def tag(self, ctx):
        """ !태그 [태그명] : 해당 태그에 대한 정보를 제공합니다. """

        embed = discord.Embed(
            title="주요 태그 목록",
            description = "다음은 코딩 테스트에서 자주 출제되는 25개의 태그 목록입니다. 각 태그명을 이용하여 문제를 추천받을 수 있습니다.",
            color=0x5c8aff
        )

        await ctx.send(embed=embed, view=TagButtonView())