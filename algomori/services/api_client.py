"""
🧩 solved.ac 등 외부 API 통신 담당
"""

import asyncio
from typing import Optional

import requests

from algomori.core.exceptions import APIError, ProblemNotFoundError


DEFAULT_MIN_SOLVED_COUNT = 0


class SolvedAcClient:
    BASE_URL = "https://solved.ac/api/v3"

    async def get_random_problem_async(
        self,
        tier: str,
        tag: Optional[str] = None,
        *,
        exclude_solved_by: Optional[str] = None,
        min_solved_count: int = DEFAULT_MIN_SOLVED_COUNT,
    ) -> dict:
        return await asyncio.to_thread(
            self.get_random_problem,
            tier,
            tag,
            exclude_solved_by=exclude_solved_by,
            min_solved_count=min_solved_count,
        )

    def get_random_problem(
        self,
        tier: str,
        tag: Optional[str] = None,
        *,
        exclude_solved_by: Optional[str] = None,
        min_solved_count: int = DEFAULT_MIN_SOLVED_COUNT,
    ) -> dict:
        query = self._build_query(
            tier=tier,
            tag=tag,
            exclude_solved_by=exclude_solved_by,
            min_solved_count=min_solved_count,
        )

        url = f"{self.BASE_URL}/search/problem"
        headers = {"x-solvedac-language": "ko"}

        params: dict[str, str] = {
            "query": query,
            "sort": "random",
            "direction": "asc",
            "limit": "1",
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("items") or data.get("count", 0) == 0:
                raise ProblemNotFoundError("문제 데이터를 찾을 수 없습니다.")

            return data["items"][0]

        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else -1
            raise APIError(status_code, str(e))
        except requests.RequestException as e:
            raise APIError(-1, str(e))

    def _build_query(
        self,
        *,
        tier: str,
        tag: Optional[str],
        exclude_solved_by: Optional[str],
        min_solved_count: int,
    ) -> str:
        tokens: list[str] = [
            "lang:ko",
            f"tier:{tier}",
        ]

        if tag:
            tokens.append(f"tag:{tag}")

        if exclude_solved_by:
            handle = exclude_solved_by.strip().lstrip("@")
            if handle:
                tokens.append(f"-@{handle}")

        if min_solved_count > 0:
            tokens.append(f"s#{min_solved_count}..")

        return " ".join(tokens)