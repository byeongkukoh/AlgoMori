import os
import discord
import requests
from dotenv import load_dotenv

# 티어 맵핑
TIER_MAP = {
    "bronze": "1..5",
    "silver": "6..10",
    "gold": "11..15",
    "platinum": "16..20",
    "diamond": "21..25",
    "ruby": "26..30",
}

# 랜덤 티어 문제 가져오기
def get_random_tier_problem(tier):
    tier_range = TIER_MAP.get(tier.lower())
    if not tier_range:
        raise ValueError(f"Invalid tier: {tier}. Valid tiers are {', '.join(TIER_MAP.keys())}.")
    
    url = f"https://solved.ac/api/v3/search/problem?query=tier:{tier_range}&sort=random&direction=asc&limit=1"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    data = response.json()
    if data["count"] == 0:
        return None
    
    problem = data["items"][0]

    return {
        "title": problem["titleKo"],
        "problemId": problem["problemId"],
        "level": problem["level"],
        "solvedac_url": f"https://solved.ac/problem_level/{problem['level']}",
        "baekjoon_url": f"https://www.acmicpc.net/problem/{problem['problemId']}"
    }


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
                await message.channel.send(f"티어 '{tier}'에 해당하는 문제를 찾을 수 없습니다.")
        except ValueError as e:
            await message.channel.send("명령어 사용 예시: `!추천 브론즈`")

# 봇 실행
client.run(TOKEN)