"""
로깅 시스템 사용 예시
"""

# 방법 1: 직접 import
from utils.logger import logger, bot, info, error, cmd, api

# 방법 2: 전체 import
from utils import logger as log

def example_usage():
    """로깅 시스템 사용 예시"""
    
    # 방법 1: 개별 함수 사용
    bot("Discord 봇을 시작합니다")
    info("일반 정보 메시지")
    error("오류가 발생했습니다")
    cmd("사용자 명령어 처리: !추천 골드")
    api("solved.ac API 호출 중...")
    
    # 방법 2: logger 객체 사용
    logger.process("PID 파일 생성됨: 12345")
    logger.config("환경변수 로드 완료")
    logger.discord("Discord 서버에 연결됨")
    
    # 방법 3: 색상 비활성화 로거
    no_color_logger = logger.Logger(enable_colors=False)
    no_color_logger.bot("색상 없는 로그 메시지")
    
    # 방법 4: 타임스탬프 없는 로거
    simple_logger = logger.Logger(enable_timestamp=False)
    simple_logger.info("간단한 로그 메시지")

if __name__ == "__main__":
    example_usage()