import discord

from datetime import time, timezone, timedelta
from discord.ext import commands, tasks

from algomori.data.tier_map import TIER_MAP
from algomori.discord.embeds import build_problem_embed
from algomori.discord.views.tier_select import TierSelectView
from algomori.core.exceptions import ConfigurationError, ProblemNotFoundError, APIError, ParseError
from algomori.core.guild_config_store import GuildConfigStore
from algomori.services.problem_service import ProblemService


class RecommenderCog(commands.Cog):
    async def cog_load(self) -> None:
        self.daily_recommendation.start()

    def cog_unload(self) -> None:
        self.daily_recommendation.cancel()

    def __init__(
        self,
        bot: commands.Bot,
        problem_service: ProblemService,
        config_store: GuildConfigStore,
    ):
        self.bot = bot
        self.problem_service = problem_service
        self.config_store = config_store

    @commands.command(name='추천')
    async def recommend(self, ctx, *args):
        """
        !추천 : 단계별 선택 인터랙션이 시작됩니다.
        !추천 [티어] : 해당 난이도(티어)의 문제를 랜덤으로 추천합니다.
        !추천 [티어] [태그] : 해당 난이도와 태그에 맞는 문제를 랜덤으로 추천합니다.
        """

        try:
            if not args:
                await ctx.send("원하는 티어를 선택하세요.", view=TierSelectView(problem_service=self.problem_service))
                return

            tier = args[0]
            tag = " ".join(args[1:]) if len(args) > 1 else None

            problem = await self.problem_service.get_random_problem(tier, tag)

            embed = build_problem_embed(problem=problem, tier=tier, tag=tag)

            await ctx.send(embed=embed)

        except (ConfigurationError, ProblemNotFoundError, APIError, ParseError) as e:
            await ctx.send(f"오류: {e}")
        except Exception as e:
            await ctx.send(
                f"""오류 발생: {e}
                명령어 예시: `!추천 브론즈` 또는 !추천 실버 다익스트라
                가능한 티어: {', '.join(TIER_MAP.keys())}"""
            )

    kst = timezone(timedelta(hours=9))

    @tasks.loop(time=[time(8, 0, 0, tzinfo=kst)])
    async def daily_recommendation(self):
        """매일 KST 오전 8시에 추천 문제를 특정 채널에 전송합니다."""

        configs = self.config_store.list_configs()
        if not configs:
            return

        for cfg in configs:
            channel = self.bot.get_channel(cfg.recommendation_channel_id)
            if channel is None:
                continue

            for tier in ["브론즈", "실버", "골드", "플래티넘"]:
                try:
                    problem = await self.problem_service.get_random_problem(tier)
                    embed = build_problem_embed(problem=problem, tier=tier)
                    await channel.send(embed=embed)
                except Exception as e:
                    await channel.send(f"`{tier}에 해당하는 문제를 찾을 수 없습니다. ({e})`")

    @daily_recommendation.before_loop
    async def before_daily_recommendation(self):
        """매일 추천 작업이 시작되기 전에 대기합니다."""

        await self.bot.wait_until_ready()
