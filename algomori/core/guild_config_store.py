from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


def validate_hhmm(value: str) -> str:
    """HH:MM(24h) 형식을 검증하고 정규화된 문자열을 반환합니다."""

    value = value.strip()
    parts = value.split(":")
    if len(parts) != 2:
        raise ValueError("시간 형식은 HH:MM 이어야 합니다.")

    hour_str, minute_str = parts
    if not hour_str.isdigit() or not minute_str.isdigit():
        raise ValueError("시간 형식은 숫자(HH:MM) 이어야 합니다.")

    hour = int(hour_str)
    minute = int(minute_str)

    if not (0 <= hour <= 23):
        raise ValueError("시간(HH)은 00~23 범위여야 합니다.")
    if not (0 <= minute <= 59):
        raise ValueError("분(MM)은 00~59 범위여야 합니다.")

    return f"{hour:02d}:{minute:02d}"


DEFAULT_CONFIG_PATH = "runtime/guild_config.json"


@dataclass(frozen=True)
class GuildConfig:
    guild_id: int
    recommendation_channel_id: int
    recommendation_time_hhmm: str


class GuildConfigStore:
    """Guild(서버)별 설정을 로컬 파일에 저장합니다.

    - BOT_TOKEN 같은 secret은 절대 저장하지 않습니다.
    - Docker/EC2에서는 파일 경로를 볼륨으로 마운트하는 형태를 권장합니다.

    저장되는 값:
    - recommendation_channel_id: 자동 추천 채널 ID
    - recommendation_time_hhmm: 자동 추천 시각(HH:MM, KST 기준)
    """

    DEFAULT_RECOMMENDATION_TIME_HHMM = "08:00"

    def __init__(self, file_path: str = DEFAULT_CONFIG_PATH):
        self._file_path = file_path

    def get_file_path(self) -> str:
        return self._file_path

    def set_recommendation_channel(self, *, guild_id: int, channel_id: int) -> None:
        data = self._load_raw()
        guild_key = str(guild_id)

        guild_entry = data.get(guild_key, {})
        guild_entry["recommendation_channel_id"] = int(channel_id)
        guild_entry.setdefault("recommendation_time_hhmm", self.DEFAULT_RECOMMENDATION_TIME_HHMM)
        data[guild_key] = guild_entry

        self._save_raw(data)

    def set_recommendation_time(self, *, guild_id: int, hhmm: str) -> None:
        hhmm = validate_hhmm(hhmm)

        data = self._load_raw()
        guild_key = str(guild_id)

        guild_entry = data.get(guild_key, {})
        guild_entry.setdefault("recommendation_channel_id", None)
        guild_entry["recommendation_time_hhmm"] = hhmm
        data[guild_key] = guild_entry

        self._save_raw(data)

    def get_recommendation_time_hhmm(self, *, guild_id: int) -> str | None:
        data = self._load_raw()
        guild_entry = data.get(str(guild_id))
        if not isinstance(guild_entry, dict):
            return None

        hhmm = guild_entry.get("recommendation_time_hhmm")
        if not isinstance(hhmm, str):
            return None

        try:
            return validate_hhmm(hhmm)
        except ValueError:
            return None

    def get_recommendation_channel_id(self, *, guild_id: int) -> int | None:
        data = self._load_raw()
        guild_entry = data.get(str(guild_id))
        if not isinstance(guild_entry, dict):
            return None

        channel_id = guild_entry.get("recommendation_channel_id")
        if channel_id is None:
            return None

        try:
            return int(channel_id)
        except (TypeError, ValueError):
            return None

    def list_configs(self) -> list[GuildConfig]:
        data = self._load_raw()
        results: list[GuildConfig] = []

        for guild_id_str, guild_entry in data.items():
            if not isinstance(guild_entry, dict):
                continue

            channel_id = guild_entry.get("recommendation_channel_id")
            if channel_id is None:
                continue

            try:
                results.append(
                    GuildConfig(
                        guild_id=int(guild_id_str),
                        recommendation_channel_id=int(channel_id),
                        recommendation_time_hhmm=validate_hhmm(
                            str(
                                guild_entry.get(
                                    "recommendation_time_hhmm",
                                    self.DEFAULT_RECOMMENDATION_TIME_HHMM,
                                )
                            )
                        ),
                    )
                )
            except (TypeError, ValueError):
                continue

        return results

    def _load_raw(self) -> dict[str, Any]:
        if not os.path.exists(self._file_path):
            return {}

        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def _save_raw(self, data: dict[str, Any]) -> None:
        directory = os.path.dirname(self._file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        tmp_path = f"{self._file_path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.replace(tmp_path, self._file_path)
