from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from algomori.domain.models.problem import Problem


class ProblemServiceInterface(ABC):
    @abstractmethod
    async def get_random_problem(self, tier: str, tag: Optional[str] = None) -> Problem:
        """티어와 태그(선택)를 바탕으로 랜덤 문제를 조회합니다."""

        ...


class ConfigInterface(ABC):
    @abstractmethod
    def get_discord_token(self) -> str:
        """운영 환경에서 주입된 Discord Bot Token을 조회합니다."""

        ...

    @abstractmethod
    def get_guild_config_path(self) -> str:
        """Guild(서버)별 설정을 저장할 파일 경로를 반환합니다."""

        ...
