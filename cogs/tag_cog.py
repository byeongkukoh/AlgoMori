import discord

from discord import ui
from discord.ext import commands, tasks


TAG_LIST = {
    # 최우선 (1-10위)
    "다이나믹 프로그래밍": "dp",
    "깊이 우선 탐색": "dfs",
    "너비 우선 탐색": "bfs",
    "이진 탐색": "binary_search",
    "그리디": "greedy",
    "투 포인터": "two_pointer",
    "백트래킹": "backtracking",
    "스택": "stack",
    "큐": "queue",
    "해시 테이블": "hash_set",
    
    # 고우선 (11-20위)
    "다익스트라": "dijkstra",
    "슬라이딩 윈도우": "sliding_window",
    "우선순위 큐": "priority_queue",
    "유니온-파인드": "disjoint_set",
    "플로이드-워셜": "floyd_warshall",
    "크루스칼": "kruskal",
    "프림": "prim",
    "위상 정렬": "topological_sorting",
    "비트마스크": "bitmask",
    "벨만-포드": "bellman_ford",
    
    # 중요 (21-30위)
    "세그먼트 트리": "segtree",
    "KMP": "kmp",
    "트라이": "trie",
    "이진 검색 트리": "tree_set",
    "펜윅 트리": "fenwick",
    "최소 공통 조상": "lca",
    "모듈러 연산": "arithmetic",
    "스위핑": "sweeping",
    "최대 유량": "flow",
    "이분 매칭": "bipartite_matching"
}


class TagButton(ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"관련 문제를 추천받으려면 `!추천 {self.label}` 명령어를 사용하세요.",
        )


class TagButtonView(ui.View):
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)

        for i, tag_name in enumerate(TAG_LIST.keys()):
            if i >= 25:
                break
            self.add_item(TagButton(label=tag_name))


class TagCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='태그')
    async def tag(self, ctx):
        """ !태그 [태그명] : 해당 태그에 대한 정보를 제공합니다. """

        embed = discord.Embed(
            title="주요 태그 목록",
            description = "다음은 코딩 테스트에서 자주 사용되는 30개의 태그 목록입니다. 각 태그명을 이용하여 문제를 추천받을 수 있습니다.",
            color=0x5c8aff
        )

        await ctx.send(embed=embed, view=TagButtonView())