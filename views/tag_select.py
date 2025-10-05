import discord

from discord import ui
from data.tag_list import TAG_LIST
from services.problem_service import ProblemService
from services.api_client import SolvedAcClient
from core.exceptions import ConfigurationError, ProblemNotFoundError, APIError, ParseError

class TagSelect(ui.Select):
    def __init__(self, tier):
        options = [discord.SelectOption(label="전체(상관없음)", value="__ALL__")]
        options += [
            discord.SelectOption(label=tag, value=tag) 
            for tag in list(TAG_LIST.keys())[:24]
        ] # 최대 25개 제한

        super().__init__(
            placeholder="원하는 알고리즘 유형을 선택하세요 (선택사항)", 
            options=options, 
            min_values=1, 
            max_values=1
        )
        
        self.tier = tier
        # 서비스 인스턴스 생성
        api_client = SolvedAcClient()
        self.problem_service = ProblemService(api_client)

    async def callback(self, interaction: discord.Interaction):
        tag = self.values[0]
        try:
            # 서비스 클래스를 통해 문제 조회 (이미 Problem 객체로 반환됨)
            problem = self.problem_service.get_random_problem(self.tier, None if tag == "__ALL__" else tag)

            embed = discord.Embed(
                title=f"{self.tier} - {tag if tag != '__ALL__' else ''} 문제 추천",
                description=f"{problem.title} (난이도: {problem.level})",
                url=problem.url,
                color=0x5c8aff
            )

            await interaction.response.edit_message(content=None, embed=embed, view=None)
            
        except (ConfigurationError, ProblemNotFoundError, APIError, ParseError) as e:
            await interaction.response.edit_message(content=f"오류: {e}", view=None)
        except Exception as e:
            await interaction.response.edit_message(content="해당 티어와 알고리즘 유형에 맞는 문제가 없습니다.", view=None)


class TagSelectView(ui.View):
    def __init__(self, tier):
        super().__init__()
        self.add_item(TagSelect(tier))