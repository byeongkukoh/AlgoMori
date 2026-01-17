from __future__ import annotations

import discord
from discord import ui

from algomori.core.guild_config_store import GuildConfigStore, normalize_hhmm_5min


class HourSelect(ui.Select):
    def __init__(self, *, wizard: "SetupWizardView", initial_hour: int):
        self.wizard = wizard
        options = [
            discord.SelectOption(label=f"{hour:02d}", value=str(hour), default=(hour == initial_hour))
            for hour in range(24)
        ]

        super().__init__(
            placeholder="시간(HH) 선택",
            options=options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.wizard.selected_hour = int(self.values[0])
        await self.wizard.render(interaction)


class MinuteSelect(ui.Select):
    def __init__(self, *, wizard: "SetupWizardView", initial_minute: int):
        self.wizard = wizard
        minutes = list(range(0, 60, 5))

        options = [
            discord.SelectOption(label=f"{m:02d}", value=str(m), default=(m == initial_minute))
            for m in minutes
        ]

        super().__init__(
            placeholder="분(MM) 선택 (5분 단위)",
            options=options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.wizard.selected_minute = int(self.values[0])
        await self.wizard.render(interaction)


class SetupWizardView(ui.View):
    """`!설정` 명령용 설정 마법사.

    순서:
    1) 채널 설정 (현재 채널)
    2) 시간 설정 (시간/분 드롭다운)
    """

    def __init__(self, *, store: GuildConfigStore, guild_id: int):
        super().__init__(timeout=300)
        self.store = store
        self.guild_id = guild_id

        self._step = 1

        # Step 2 state
        initial_hhmm = (
            self.store.get_recommendation_time_hhmm(guild_id=self.guild_id)
            or self.store.DEFAULT_RECOMMENDATION_TIME_HHMM
        )

        hour_str, minute_str = initial_hhmm.split(":")
        self.selected_hour = int(hour_str)
        self.selected_minute = int(minute_str)

        self.hour_select = HourSelect(wizard=self, initial_hour=self.selected_hour)
        self.minute_select = MinuteSelect(wizard=self, initial_minute=self.selected_minute)

        self.add_item(self.hour_select)
        self.add_item(self.minute_select)

        self._sync_controls()

    def build_initial_message(self) -> str:
        channel_id = self.store.get_recommendation_channel_id(guild_id=self.guild_id)
        time_hhmm = (
            self.store.get_recommendation_time_hhmm(guild_id=self.guild_id)
            or self.store.DEFAULT_RECOMMENDATION_TIME_HHMM
        )

        return self._build_content(channel_id=channel_id, time_hhmm=time_hhmm)

    def _build_content(self, *, channel_id: int | None, time_hhmm: str) -> str:
        channel_text = f"<#{channel_id}>" if channel_id else "(미설정)"

        return (
            "설정 마법사\n"
            f"- 자동 추천 채널: {channel_text}\n"
            f"- 자동 추천 시간(KST): {time_hhmm}\n\n"
            "순서대로 진행하세요."
        )

    def _sync_controls(self) -> None:
        for child in self.children:
            if isinstance(child, ui.Button):
                if child.custom_id == "setup:set_channel":
                    child.disabled = self._step != 1
                elif child.custom_id == "setup:save_time":
                    child.disabled = self._step != 2
                elif child.custom_id == "setup:finish":
                    child.disabled = self._step != 3

            if isinstance(child, ui.Select):
                child.disabled = self._step != 2

    async def render(self, interaction: discord.Interaction) -> None:
        channel_id = self.store.get_recommendation_channel_id(guild_id=self.guild_id)
        time_hhmm = (
            self.store.get_recommendation_time_hhmm(guild_id=self.guild_id)
            or self.store.DEFAULT_RECOMMENDATION_TIME_HHMM
        )

        content = self._build_content(channel_id=channel_id, time_hhmm=time_hhmm)
        self._sync_controls()
        await interaction.response.edit_message(content=content, view=self)

    @ui.button(label="1) 이 채널로 설정", style=discord.ButtonStyle.primary, custom_id="setup:set_channel")
    async def set_channel(self, interaction: discord.Interaction, button: ui.Button) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("서버에서만 사용할 수 있습니다.", ephemeral=True)
            return

        if not isinstance(interaction.channel, (discord.TextChannel, discord.Thread)):
            await interaction.response.send_message("텍스트 채널에서만 설정할 수 있습니다.", ephemeral=True)
            return

        self.store.set_recommendation_channel(
            guild_id=interaction.guild.id,
            channel_id=interaction.channel.id,
        )

        self._step = 2
        await self.render(interaction)

    @ui.button(label="2) 시간 저장", style=discord.ButtonStyle.primary, custom_id="setup:save_time")
    async def save_time(self, interaction: discord.Interaction, button: ui.Button) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("서버에서만 사용할 수 있습니다.", ephemeral=True)
            return

        hhmm_candidate = f"{self.selected_hour:02d}:{self.selected_minute:02d}"

        try:
            hhmm = normalize_hhmm_5min(hhmm_candidate)
        except ValueError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return

        self.store.set_recommendation_time(guild_id=interaction.guild.id, hhmm=hhmm)
        self._step = 3
        await self.render(interaction)

    @ui.button(label="완료", style=discord.ButtonStyle.success, custom_id="setup:finish")
    async def finish(self, interaction: discord.Interaction, button: ui.Button) -> None:
        self.stop()
        await interaction.response.edit_message(content="설정이 완료되었습니다.", view=None)

    @ui.button(label="취소", style=discord.ButtonStyle.secondary, custom_id="setup:cancel")
    async def cancel(self, interaction: discord.Interaction, button: ui.Button) -> None:
        self.stop()
        await interaction.response.edit_message(content="설정을 취소했습니다.", view=None)

    async def on_timeout(self) -> None:
        for child in self.children:
            if isinstance(child, (ui.Button, ui.Select)):
                child.disabled = True
