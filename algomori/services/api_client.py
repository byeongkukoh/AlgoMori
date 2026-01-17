"""
🧩 solved.ac 등 외부 API 통신 담당
"""

import requests

from typing import Optional
from algomori.core.exceptions import APIError, ProblemNotFoundError

class SolvedAcClient:
    BASE_URL = "https://solved.ac/api/v3"

    def get_random_problem(self, tier: str, tag: Optional[str] = None) -> dict:
        # 쿼리 생성
        if tag:
            query = f"lang:ko+tier:{tier}+tag:{tag}"
        else:
            query = f"lang:ko+tier:{tier}"

        # API 호출 및 예외 처리 구현
        url = f"{self.BASE_URL}/search/problem?query={query}&sort=random&direction=asc&limit=1"

        # headers 추가
        headers = {"x-solvedac-language": "ko"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            if not data.get('items') or data.get('count', 0) == 0:
                raise ProblemNotFoundError("문제 데이터를 찾을 수 없습니다.")
            
            return data['items'][0]
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else -1
            raise APIError(status_code, str(e))
        except requests.RequestException as e:
            raise APIError(-1, str(e))