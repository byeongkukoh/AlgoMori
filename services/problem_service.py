from typing import Optional

from core.interface import ProblemServiceInterface
from core.exceptions import ConfigurationError
from services.api_client import SolvedAcClient
from services.parsers import parse_problem
from data.tier_map import TIER_MAP
from data.tag_list import TAG_LIST

class ProblemService(ProblemServiceInterface):
    def __init__(self, api_client: SolvedAcClient):
        self.api_client = api_client

    def get_random_problem(self, tier: str, tag: Optional[str] = None):
        # 티어 검증 및 변환
        tier_range = TIER_MAP.get(tier.lower())
        if not tier_range:
            raise ConfigurationError(f"유효하지 않은 티어입니다: {tier}. 가능한 티어: {', '.join(TIER_MAP.keys())}")

        # 태그 검증 및 변환 (옵션)
        en_tag = None
        if tag:
            en_tag = TAG_LIST.get(tag)

            if not en_tag:
                raise ConfigurationError(f"유효하지 않은 태그입니다: {tag}. 가능한 태그: {', '.join(TAG_LIST.keys())}")
            
        # API 클라이언트에 티어 범위와 태그 전달
        data = self.api_client.get_random_problem(tier_range, en_tag)
        return parse_problem(data)