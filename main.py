import discord

from discord.ext import commands
from config import DISCORD_BOT_TOKEN
from cogs.recommender_cog import RecommenderCog
from cogs.tag_cog import TagCog


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name}로 로그인되었습니다. (ID: {bot.user.id})')

    # Start the daily recommendation task
    await bot.add_cog(RecommenderCog(bot))
    await bot.add_cog(TagCog(bot))

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)