from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


DEFAULT_CONFIG_PATH = "runtime/guild_config.json"


@dataclass(frozen=True)
class GuildConfig:
    guild_id: int
    recommendation_channel_id: int


class GuildConfigStore:
    """Guild(서버)별 설정을 로컬 파일에 저장합니다.

    - BOT_TOKEN 같은 secret은 절대 저장하지 않습니다.
    - Docker/EC2에서는 파일 경로를 볼륨으로 마운트하는 형태를 권장합니다.
    """

    def __init__(self, file_path: str = DEFAULT_CONFIG_PATH):
        self._file_path = file_path

    def get_file_path(self) -> str:
        return self._file_path

    def set_recommendation_channel(self, *, guild_id: int, channel_id: int) -> None:
        data = self._load_raw()
        guild_key = str(guild_id)

        guild_entry = data.get(guild_key, {})
        guild_entry["recommendation_channel_id"] = int(channel_id)
        data[guild_key] = guild_entry

        self._save_raw(data)

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
