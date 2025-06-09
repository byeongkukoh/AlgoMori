import os
import discord
import asyncio

from dotenv import load_dotenv
from recommender import get_random_tier_problem, TIER_MAP
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 환경 변수(.env)에서 토큰 불러오기
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    raise ValueError("디스코드 봇 토큰이 잘못되었습니다. 토큰을 확인해주세요.")

# intents 선언 (디스코드 API 정책상 필수)
intents = discord.Intents.default()
intents.message_content = True  # 일반 메시지 접근 허용

# 클라이언트 객체 생성
client = discord.Client(intents=intents)

TARGET_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', '0'))

# 자동 추천 함수
async def send_daily_recommendation():
    await client.wait_until_ready()
    channel = client.get_channel(TARGET_CHANNEL_ID)

    if channel is None:
        print("채널을 찾을 수 없습니다. DISCORD_CHANNEL_ID를 확인하세요.")
        return
    
    # 여러 난이도 순차 추천
    for tier in ["브론즈", "실버", "골드", "플래티넘", "다이아", "루비"]:
        try:
            problem = get_random_tier_problem(tier)

            if problem:
                print("문제를 불러왔습니다.")

                embed = discord.Embed(
                    title=f"{tier.title()} 추천 문제",
                    description=f"{problem['title']} (난이도: {problem['level']})",
                    url=problem['baekjoon_url'],
                    color=0x5c8aff,
                )

                print("임베드를 생성했습니다.")

                await channel.send(embed=embed)

                print("추천 문제를 전송했습니다.")
            else:
                print(f"'{tier}'에 해당하는 문제를 찾을 수 없습니다.")

            await asyncio.sleep(2)
        except:
            print("알 수 없는 오류가 발생했습니다.")
        

@client.event
async def on_ready():
    print(f'{client.user}로 로그인되었습니다!')
    scheduler = AsyncIOScheduler(timezone='Asia/Seoul')
    scheduler.add_job(send_daily_recommendation, 'cron', hour=17, minute=22)
    scheduler.start()

@client.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author == client.user:
        return
    
    # 테스트용 명령어
    if message.content == "!test":
        await message.channel.send("봇이 정상적으로 동작합니다.")

    # !추천 [난이도] 명령어 처리
    if message.content.startswith("!추천"):
        try:
            _, tier = message.content.split()
            problem = get_random_tier_problem(tier)
            if problem:
                await message.channel.send(
                    f"**문제 추천**\n"
                    f"제목: {problem['title']}\n"
                    f"난이도: {problem['level']}\n"
                    f"Solving URL: {problem['solvedac_url']}\n"
                    f"Baekjoon URL: {problem['baekjoon_url']}"
                )
            else:
                await message.channel.send(f"'{tier}'에 해당하는 문제를 찾을 수 없습니다.")
        except ValueError as e:
            await message.channel.send(
                "명령어 사용 예시: `!추천 브론즈`\n"
                f"가능한 티어: {', '.join(TIER_MAP.keys())}"
            )
        except Exception:
            await message.channel.send("알 수 없는 오류가 발생했습니다.")

# 봇 실행
client.run(TOKEN)