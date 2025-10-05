import os
from dotenv import load_dotenv
from .interface import ConfigInterface
from .exceptions import ConfigurationError

class Config(ConfigInterface):
    def __init__(self):
        load_dotenv()
        self._validate_config()

    def _validate_config(self):
        """
        📌 환경변수 검증을 수행
        환경변수가 있는지 확인하고 없으면 ConfigurationError를 발생시킵니다.
        """
        missing_vars = []

        if not os.getenv('DISCORD_BOT_TOKEN'):
            missing_vars.append('DISCORD_BOT_TOKEN')

        if not os.getenv('DISCORD_CHANNEL_ID'):
            missing_vars.append('DISCORD_CHANNEL_ID')

        if missing_vars:
            raise ConfigurationError(
                f"필수 환경변수가 누락되었습니다: {', '.join(missing_vars)}\n"
                f"환경변수(.env)를 확인해주세요."
            )

    def get_discord_token(self) -> str:
        """
        📌 .env 파일에 정의된 Discord Bot Token을 조회
        """
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            raise ConfigurationError("DISCORD_BOT_TOKEN이 설정되지 않았습니다.")
        
        return token
    
    def get_discord_channel_id(self) -> str:
        """
        📌 .env 파일에 정의된 Discord Channel ID를 조회
        """
        channel_id = os.getenv('DISCORD_CHANNEL_ID')
        if not channel_id:
            raise ConfigurationError("DISCORD_CHANNEL_ID가 설정되지 않았습니다.")
        
        try:
            return int(channel_id)
        except ValueError:
            raise ConfigurationError(f"DISCORD_CHANNEL_ID는 숫자여야 합니다: {channel_id}")