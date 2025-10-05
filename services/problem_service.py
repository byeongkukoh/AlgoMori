import requests
from data.tag_list import TAG_LIST
from data.tier_map import TIER_MAP, TIERS

# request header 설정
headers = {
    "x-solvedac-language": "ko",
}

# 랜덤 티어 문제 가져오기
def get_random_problem(tier, tag=None):
    tier_range = TIER_MAP.get(tier.lower())
    if not tier_range:
        raise ValueError(f"Invalid tier: {tier}. Valid tiers are {', '.join(TIER_MAP.keys())}.")
    
    if tag:
        en_tag = TAG_LIST.get(tag)
        url = f"https://solved.ac/api/v3/search/problem?query=lang:ko+tier:{tier_range}+tag:{en_tag}&sort=random&direction=asc&limit=1"
    else:
        url = f"https://solved.ac/api/v3/search/problem?query=lang:ko+tier:{tier_range}&sort=random&direction=asc&limit=1"
    
    response = requests.get(url, headers=headers)
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