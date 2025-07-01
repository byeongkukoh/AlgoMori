import discord

from discord import ui
from views.tag_select import TagSelectView

from data.tier_map import TIERS

class TierSelect(ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=tier, value=tier) for tier in TIERS]

        super().__init__(
            placeholder="원하는 티어를 선택하세요", 
            options=options, 
            min_values=1, 
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        tier = self.values[0]

        await interaction.response.edit_message(
            content=f"선택한 티어: {tier}\n알고리즘 유형을 선택하세요.",
            view=TagSelectView(tier=tier)
        )


class TierSelectView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TierSelect())