import os
import discord
from dotenv import load_dotenv

# 환경 변수(.env)에서 토큰 불러오기
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable not set.")

# intents 선언 (디스코드 API 정책상 필수)
intents = discord.Intents.default()
intents.message_content = True  # 일반 메시지 접근 허용

# 클라이언트 객체 생성
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user}로 로그인되었습니다!')

@client.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author == client.user:
        return
    
    # 테스트용 명령어
    if message.content == "!test":
        await message.channel.send("봇이 정상적으로 동작합니다.")

# 봇 실행
client.run(TOKEN)