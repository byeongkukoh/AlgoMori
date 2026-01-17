from __future__ import annotations

import discord

from algomori.domain.models.problem import Problem


EMBED_COLOR = 0x5C8AFF


def build_problem_embed(*, problem: Problem, tier: str, tag: str | None = None) -> discord.Embed:
    title = f"{tier.title()} 문제 추천" + (f" - {tag}" if tag else "")

    return discord.Embed(
        title=title,
        description=f"{problem.title} (난이도: {problem.level})",
        url=problem.url,
        color=EMBED_COLOR,
    )
