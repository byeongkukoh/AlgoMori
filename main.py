import discord
import asyncio

from aiohttp import web
from discord.ext import commands
from config import DISCORD_BOT_TOKEN
from cogs.recommender_cog import RecommenderCog


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name}로 로그인되었습니다. (ID: {bot.user.id})')

    # Start the daily recommendation task
    await bot.add_cog(RecommenderCog(bot))


# aiohttp 핑 서버
async def ping(request):
    return web.Response(text="Pong!")

async def run_web():
    app = web.Application()
    app.router.add_get('/ping', ping)
    runner = web.AppRunner(app)

    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)

    await site.start()
    print("Health check server running on http://0.0.0.0:8000")


# bot과 server 동시 실행
async def main():
    await asyncio.gather(
        bot.start(DISCORD_BOT_TOKEN),
        run_web()
    )

if __name__ == "__main__":
    asyncio.run(main())