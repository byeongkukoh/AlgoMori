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

    async def get_random_problem(
        self,
        tier: str,
        tag: Optional[str] = None,
        exclude_solved_by: Optional[str] = None,
        min_solved_count: int | None = None,
    ) -> Problem:
        tier = tier.strip()
        tag = tag.strip() if tag else None
        exclude_solved_by = exclude_solved_by.strip() if exclude_solved_by else None

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

        if min_solved_count is None:
            # 기존 동작 유지: 유저 기반 추천(안 푼 문제)인 경우에만 너무 마이너한 문제를 피하려고
            # solved count 10,000 이상 필터를 기본 적용합니다.
            min_solved_count = 10000 if exclude_solved_by else 0

        data = await self.api_client.get_random_problem_async(
            tier_range,
            en_tag,
            exclude_solved_by=exclude_solved_by,
            min_solved_count=min_solved_count,
        )

        return parse_problem(data)
