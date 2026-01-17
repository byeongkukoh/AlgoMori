import discord
from discord.ext import commands

from algomori.discord.views.tag_buttons import TagButtonView


class TagCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="태그")
    async def tag(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="주요 태그 목록",
            description=(
                "다음은 코딩 테스트에서 자주 출제되는 25개의 태그 목록입니다. "
                "각 태그명을 이용하여 문제를 추천받을 수 있습니다."
            ),
            color=0x5C8AFF,
        )

        await ctx.send(embed=embed, view=TagButtonView())
