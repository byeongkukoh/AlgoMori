from __future__ import annotations

import discord
from discord import ui

from algomori.core.guild_config_store import GuildConfigStore, validate_hhmm


class _TimeModal(ui.Modal, title="자동 추천 시간 설정"):
    time_hhmm = ui.TextInput(
        label="시간(HH:MM, KST)",
        placeholder="예: 08:00",
        required=True,
        max_length=5,
    )

    def __init__(self, *, initial_value: str, on_submit_callback):
        super().__init__()
        self.time_hhmm.default = initial_value
        self._on_submit_callback = on_submit_callback

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self._on_submit_callback(interaction, str(self.time_hhmm.value))


class SetupWizardView(ui.View):
    """`!설정` 명령용 설정 마법사.

    순서:
    1) 채널 설정 (현재 채널)
    2) 시간 설정 (HH:MM)
    """

    def __init__(self, *, store: GuildConfigStore, guild_id: int):
        super().__init__(timeout=300)
        self.store = store
        self.guild_id = guild_id

        self._step = 1
        self._sync_buttons()

    def _sync_buttons(self) -> None:
        for child in self.children:
            if isinstance(child, ui.Button):
                if child.custom_id == "setup:set_channel":
                    child.disabled = self._step != 1
                elif child.custom_id == "setup:set_time":
                    child.disabled = self._step != 2
                elif child.custom_id == "setup:finish":
                    child.disabled = self._step != 3

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

    async def _render(self, interaction: discord.Interaction) -> None:
        channel_id = self.store.get_recommendation_channel_id(guild_id=self.guild_id)
        time_hhmm = (
            self.store.get_recommendation_time_hhmm(guild_id=self.guild_id)
            or self.store.DEFAULT_RECOMMENDATION_TIME_HHMM
        )

        content = self._build_content(channel_id=channel_id, time_hhmm=time_hhmm)

        self._sync_buttons()
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
        await self._render(interaction)

    @ui.button(label="2) 시간 설정", style=discord.ButtonStyle.primary, custom_id="setup:set_time")
    async def set_time(self, interaction: discord.Interaction, button: ui.Button) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("서버에서만 사용할 수 있습니다.", ephemeral=True)
            return

        initial_value = (
            self.store.get_recommendation_time_hhmm(guild_id=interaction.guild.id)
            or self.store.DEFAULT_RECOMMENDATION_TIME_HHMM
        )

        async def _on_submit(interaction2: discord.Interaction, value: str) -> None:
            try:
                hhmm = validate_hhmm(value)
            except ValueError as e:
                await interaction2.response.send_message(str(e), ephemeral=True)
                return

            self.store.set_recommendation_time(guild_id=interaction.guild.id, hhmm=hhmm)
            self._step = 3
            await self._render(interaction2)

        await interaction.response.send_modal(_TimeModal(initial_value=initial_value, on_submit_callback=_on_submit))

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
            if isinstance(child, ui.Button):
                child.disabled = True
