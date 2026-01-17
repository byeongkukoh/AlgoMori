from __future__ import annotations

import os

from dotenv import load_dotenv

from algomori.core.exceptions import ConfigurationError
from algomori.core.interface import ConfigInterface


DISCORD_BOT_TOKEN_ENV = "DISCORD_BOT_TOKEN"
ALGOMORI_GUILD_CONFIG_PATH_ENV = "ALGOMORI_GUILD_CONFIG_PATH"


class Config(ConfigInterface):
    def __init__(self) -> None:
        load_dotenv()

        token = os.getenv(DISCORD_BOT_TOKEN_ENV)
        if token is None or token == "":
            raise ConfigurationError(
                f"필수 환경변수가 누락되었습니다: {DISCORD_BOT_TOKEN_ENV}\n환경변수(.env)를 확인해주세요."
            )

        self._discord_bot_token = token

        # Guild 설정(JSON) 파일 경로 (채널 설정은 Discord에서 하고, 여기에는 저장만 함)
        self._guild_config_path = os.getenv(ALGOMORI_GUILD_CONFIG_PATH_ENV) or "runtime/guild_config.json"

    def get_discord_token(self) -> str:
        return self._discord_bot_token

    def get_guild_config_path(self) -> str:
        return self._guild_config_path
