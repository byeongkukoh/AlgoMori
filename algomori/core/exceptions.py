"""
🧩 커스텀 예외 클래스 정의
"""

class AlgoMoriException(Exception):
    """
    📌 AlgoMori 프로젝트의 기본 예외 클래스
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ConfigurationError(AlgoMoriException):
    """
    📌 설정 관련 오류를 반환 (환경변수 누락 등)
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ProblemNotFoundError(AlgoMoriException):
    """
    📌 문제를 찾을 수 없을 때 발생하는 오류
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class APIError(AlgoMoriException):
    """
    📌 solved.ac API 호출 실패 시 발생하는 오류
    """
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"APIError {status_code}: {message}")
    

class ParseError(AlgoMoriException):
    """
    📌 API 응답 파싱 실패 시 발생하는 오류
    """

    def __init__(self, message: str = "데이터 파싱에 실패했습니다."):
        self.message = message
        super().__init__(self.message)