"""
🧩 문제 데이터를 담는 데이터 클래스
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Problem:
    id: int
    title: str
    level: int
    url: str
    tags: List[str]