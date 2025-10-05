import discord

from data.tag_list import TAG_LIST
from data.tier_map import TIER_MAP, TIERS

from views.tier_select import TierSelectView
from datetime import time, timezone, timedelta
from core.config import DISCORD_CHANNEL_ID
from discord.ext import commands, tasks
from services.problem_service import get_random_problem


class RecommenderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_recommendation.start()   # 자동 추천 기능

    @commands.command(name='추천')
    async def recommend(self, ctx, *args):
        """
        !추천 : 단계별 선택 인터랙션이 시작됩니다.
        !추천 [티어] : 해당 난이도(티어)의 문제를 랜덤으로 추천합니다.
        !추천 [티어] [태그] : 해당 난이도와 태그에 맞는 문제를 랜덤으로 추천합니다.
        """
        try:
            if not args:
                await ctx.send("원하는 티어를 선택하세요.", view=TierSelectView())
                return
            
            tier = args[0]
            tag = " ".join(args[1:]) if len(args) > 1 else None

            problem = get_random_problem(tier, tag)
            if problem:
                embed = discord.Embed(
                    title = f"{tier.title()} 문제 추천" + (f" - {tag}" if tag else ""),
                    description = f"{problem['title']} (난이도: {problem['level']})",
                    url = problem['baekjoon_url'],
                    color=0x5c8aff
                )

                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    f"`{tier}{' ' + tag if tag else ''}에 해당하는 문제를 찾을 수 없습니다. 다시 시도해주세요.`"
                )
        except Exception as e:
            await ctx.send(
                f"""오류 발생: {e}
                명령어 예시: `!추천 브론즈` 또는 !추천 실버 디익스트라
                가능한 티어: {', '.join(TIER_MAP.keys())}"""
            )

    kst = timezone(timedelta(hours=9))
    @tasks.loop(time=[time(8, 0, 0, tzinfo=kst)]) # KST 시간대로 수정
    async def daily_recommendation(self):
        """ 매일 KST 오전 8시에 추천 문제를 특정 채널에 전송합니다. """
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID)
        
        for tier in ["브론즈", "실버", "골드", "플래티넘"]:
            problem = get_random_problem(tier)
            if problem:
                embed = discord.Embed(
                    title = f"{tier.title()} 문제 추천",
                    description = f"{problem['title']} (난이도: {problem['level']})",
                    url = problem['baekjoon_url'],
                    color=0x5c8aff
                )

                await channel.send(embed=embed)

            else:
                await channel.send(
                    f"`{tier}에 해당하는 문제를 찾을 수 없습니다. 다시 시도해주세요.`"
                )

    @daily_recommendation.before_loop
    async def before_daily_recommendation(self):
        """ 매일 추천 작업이 시작되기 전에 대기합니다. """
        await self.bot.wait_until_ready()