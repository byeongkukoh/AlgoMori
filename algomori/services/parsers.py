"""
🧩 API 응답 dict를 Problem 객체로 변환
"""

from typing import Any

from algomori.domain.models.problem import Problem
from algomori.core.exceptions import ParseError


def parse_problem(data: dict[str, Any]) -> Problem:
    try:
        raw_problem_id = data["problemId"]
        problem_id = int(raw_problem_id)

        return Problem(
            id=problem_id,
            title=data.get("titleKo", ""),
            level=data.get("level", 0),
            url=f"https://www.acmicpc.net/problem/{problem_id}",
            tags=[tag["key"] for tag in data.get("tags", [])],
        )
    except Exception as e:
        raise ParseError(f"문제 데이터 파싱 실패: {e}") from e