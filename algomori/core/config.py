from __future__ import annotations

import os

from dotenv import load_dotenv

from algomori.core.exceptions import ConfigurationError
from algomori.core.interface import ConfigInterface


DISCORD_BOT_TOKEN_ENV = "DISCORD_BOT_TOKEN"
DISCORD_CHANNEL_ID_ENV = "DISCORD_CHANNEL_ID"


class Config(ConfigInterface):
    def __init__(self) -> None:
        load_dotenv()

        token = os.getenv(DISCORD_BOT_TOKEN_ENV)
        channel_id_raw = os.getenv(DISCORD_CHANNEL_ID_ENV)

        missing_vars: list[str] = []
        if token is None or token == "":
            missing_vars.append(DISCORD_BOT_TOKEN_ENV)
        if channel_id_raw is None or channel_id_raw == "":
            missing_vars.append(DISCORD_CHANNEL_ID_ENV)

        if missing_vars:
            raise ConfigurationError(
                "필수 환경변수가 누락되었습니다: {missing}\n환경변수(.env)를 확인해주세요.".format(
                    missing=", ".join(missing_vars)
                )
            )

        assert token is not None
        assert channel_id_raw is not None

        try:
            channel_id = int(channel_id_raw)
        except ValueError as e:
            raise ConfigurationError(f"{DISCORD_CHANNEL_ID_ENV}는 숫자여야 합니다: {channel_id_raw}") from e

        self._discord_bot_token = token
        self._discord_channel_id = channel_id

    def get_discord_token(self) -> str:
        return self._discord_bot_token

    def get_discord_channel_id(self) -> int:
        return self._discord_channel_id
