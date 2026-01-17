from __future__ import annotations

from typing import Optional

from algomori.core.exceptions import ConfigurationError
from algomori.core.interface import ProblemServiceInterface
from algomori.data.tag_list import TAG_LIST
from algomori.data.tier_map import TIER_MAP
from algomori.domain.models.problem import Problem
from algomori.services.api_client import SolvedAcClient
from algomori.services.parsers import parse_problem


class ProblemService(ProblemServiceInterface):
    def __init__(self, api_client: SolvedAcClient):
        self.api_client = api_client

    async def get_random_problem(self, tier: str, tag: Optional[str] = None) -> Problem:
        tier = tier.strip()
        tag = tag.strip() if tag else None

        tier_range = TIER_MAP.get(tier)
        if not tier_range:
            raise ConfigurationError(
                f"유효하지 않은 티어입니다: {tier}. 가능한 티어: {', '.join(TIER_MAP.keys())}"
            )

        en_tag: str | None = None
        if tag:
            en_tag = TAG_LIST.get(tag)
            if not en_tag:
                raise ConfigurationError(
                    f"유효하지 않은 태그입니다: {tag}. 가능한 태그: {', '.join(TAG_LIST.keys())}"
                )

        data = await self.api_client.get_random_problem_async(tier_range, en_tag)
        return parse_problem(data)