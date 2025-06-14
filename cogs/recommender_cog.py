import discord

from datetime import time
from config import DISCORD_CHANNEL_ID
from discord.ext import commands, tasks
from services.get_random_problem import get_random_problem, TIER_MAP


class RecommenderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='추천')
    async def recommend(self, ctx, *args):
        """ !추천 [티어] : 해당 난이도(티어)의 문제를 랜덤으로 추천합니다. """
        try:
            if not args:
                await ctx.send("티어를 입력해주세요. 예시 `!추천 브론즈`")
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

    @tasks.loop(time=[time(23, 0, 0)]) # UTC+0(=KST-9), 시간대 맞게 수정
    async def daily_recommendation(self):
        """ 매일 정오에 추천 문제를 특정 채널에 전송합니다. """
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