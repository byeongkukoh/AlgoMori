import asyncio

import discord

from datetime import datetime, timezone, timedelta
from discord.ext import commands, tasks

from algomori.data.tier_map import TIER_MAP
from algomori.discord.embeds import build_problem_embed
from algomori.discord.views.alio_olio import AlioOlioView
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
        self._last_sent_by_guild_and_time: dict[tuple[int, str], str] = {}

    @commands.command(name='추천')
    async def recommend(self, ctx, *args):
        """
        !추천 : 단계별 선택 인터랙션이 시작됩니다.
        !추천 [티어] : 해당 난이도(티어)의 문제를 랜덤으로 추천합니다.
        !추천 [티어] [태그] : 해당 난이도와 태그에 맞는 문제를 랜덤으로 추천합니다.
        !추천 [티어] [태그] @boj_id : (선택) 특정 유저가 안 푼 문제 추천 (10,000명+ 푼 문제만)
        """

        try:
            if not args:
                await ctx.send("원하는 티어를 선택하세요.", view=TierSelectView(problem_service=self.problem_service))
                return

            if args[0] == "알리오골리오":
                view = AlioOlioView(problem_service=self.problem_service)
                await ctx.send(view.build_initial_message(), view=view)
                return

            tier = args[0]

            exclude_solved_by: str | None = None

            tag_tokens = list(args[1:])
            if tag_tokens and tag_tokens[-1].startswith("@"): 
                candidate = tag_tokens[-1].lstrip("@").strip()
                if candidate:
                    exclude_solved_by = candidate
                    tag_tokens = tag_tokens[:-1]

            tag = " ".join(tag_tokens) if tag_tokens else None

            problem = await self.problem_service.get_random_problem(
                tier,
                tag,
                exclude_solved_by=exclude_solved_by,
            )

            embed = build_problem_embed(problem=problem, tier=tier, tag=tag)

            await ctx.send(embed=embed)

        except (ConfigurationError, ProblemNotFoundError, APIError, ParseError) as e:
            await ctx.send(f"오류: {e}")
        except Exception as e:
            await ctx.send(
                f"""오류 발생: {e}
                명령어 예시: `!추천 브론즈` 또는 `!추천 실버 다익스트라` 또는 `!추천 실버 @boj_id`
                가능한 티어: {', '.join(TIER_MAP.keys())}"""
            )

    kst = timezone(timedelta(hours=9))

    @tasks.loop(minutes=5)
    async def daily_recommendation(self):
        """설정된 시각(KST)에 자동 추천을 전송합니다."""

        now = datetime.now(self.kst)
        now_hhmm = now.strftime("%H:%M")
        today = now.strftime("%Y-%m-%d")

        configs = self.config_store.list_configs()
        if not configs:
            return

        for cfg in configs:
            if cfg.recommendation_time_hhmm != now_hhmm:
                continue

            key = (cfg.guild_id, cfg.recommendation_time_hhmm)
            if self._last_sent_by_guild_and_time.get(key) == today:
                continue

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

            self._last_sent_by_guild_and_time[key] = today

    @daily_recommendation.before_loop
    async def before_daily_recommendation(self):
        """루프를 5분 경계에 맞춰 시작합니다."""

        await self.bot.wait_until_ready()

        now = datetime.now(self.kst)
        minutes_to_wait = (5 - (now.minute % 5)) % 5
        seconds_to_wait = minutes_to_wait * 60 - now.second - (now.microsecond / 1_000_000)
        if seconds_to_wait < 0:
            seconds_to_wait += 300

        if seconds_to_wait > 0:
            await asyncio.sleep(seconds_to_wait)
