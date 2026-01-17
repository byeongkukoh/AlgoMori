"""
🧩 API 응답 dict를 Problem 객체로 변환
"""

from algomori.domain.models.problem import Problem
from algomori.core.exceptions import ParseError

def parse_problem(data: dict) -> Problem:
    try:
        return Problem(
            id = data.get('problemId'),
            title = data.get('titleKo', ''),
            level = data.get('level', 0),
            url=f"https://www.acmicpc.net/problem/{data.get('problemId')}",
            tags=[tag['key'] for tag in data.get('tags', [])]
        )
    except Exception as e:
        raise ParseError(f"문제 데이터 파싱 실패: {e}")