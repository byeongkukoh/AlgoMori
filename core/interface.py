from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

"""
🧩 문제 서비스 인터페이스
"""
class ProblemServiceInterface(ABC):
    @abstractmethod
    async def get_random_problem(self, tier: str, tag: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        📌 티어와 태그(선택)를 바탕으로 랜덤으로 문제를 조회
        """
        pass


"""
🧩 설정 인터페이스
"""
class ConfigInterface(ABC):
    @abstractmethod
    def get_discord_token(self) -> str:
        """
        📌 .env 파일에 정의된 Discord Bot Token을 조회
        """
        pass
        
        
    @abstractmethod
    def get_discord_channel_id(self) -> int:
        """
        📌 .env 파일에 정의된 Discord Channel ID를 조회
        """
        pass