from __future__ import annotations

import discord
from discord.ext import commands

from algomori.core.guild_config_store import GuildConfigStore


class SettingsCog(commands.Cog):
    def __init__(self, bot: commands.Bot, config_store: GuildConfigStore):
        self.bot = bot
        self.config_store = config_store

    @commands.command(name="설정채널")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def set_recommendation_channel(self, ctx: commands.Context) -> None:
        """매일 자동 추천이 전송될 채널을 현재 채널로 설정합니다."""

        assert ctx.guild is not None

        channel = ctx.channel
        if not isinstance(channel, (discord.TextChannel, discord.Thread)):
            await ctx.send("이 명령은 텍스트 채널에서만 사용할 수 있습니다.")
            return

        self.config_store.set_recommendation_channel(
            guild_id=ctx.guild.id,
            channel_id=channel.id,
        )

        await ctx.send(f"자동 추천 채널을 {channel.mention}로 설정했습니다.")

    @set_recommendation_channel.error
    async def set_recommendation_channel_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("권한이 없습니다. (서버 관리 권한 필요: Manage Server)")
            return

        raise error

    @commands.command(name="설정보기")
    @commands.guild_only()
    async def show_settings(self, ctx: commands.Context) -> None:
        """현재 서버의 설정을 표시합니다."""

        assert ctx.guild is not None

        channel_id = self.config_store.get_recommendation_channel_id(guild_id=ctx.guild.id)
        if channel_id is None:
            await ctx.send("자동 추천 채널이 아직 설정되지 않았습니다. `!설정채널`을 실행하세요.")
            return

        channel = self.bot.get_channel(channel_id)
        if channel is None:
            await ctx.send(f"자동 추천 채널 ID: {channel_id} (채널을 찾지 못했습니다)")
            return

        await ctx.send(f"자동 추천 채널: {channel.mention}")
