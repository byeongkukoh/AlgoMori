from __future__ import annotations


def format_problem_level(level: int) -> str:
    """solved.ac level(int)을 사람이 읽기 좋은 한글 티어로 표시합니다.

    Examples:
    - level=5  -> "브론즈1 (5)"
    - level=6  -> "실버5 (6)"
    - level=30 -> "루비1 (30)"

    Note:
    - solved.ac 기준: 1=Bronze V ... 30=Ruby I
    """

    if level <= 0:
        return f"Unrated ({level})"

    tiers = ["브론즈", "실버", "골드", "플래티넘", "다이아", "루비"]

    # 1..30 -> group 0..5, within 0..4
    idx = level - 1
    group = idx // 5
    within = idx % 5

    if group < 0 or group >= len(tiers):
        return f"Unknown ({level})"

    # within: 0..4 corresponds to 5..1
    tier_number = 5 - within
    return f"{tiers[group]}{tier_number} ({level})"
