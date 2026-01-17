"""
AlgoMori Discord Bot - 통합 로깅 시스템
색상 코드와 로그 레벨을 포함한 통합 로거
"""

import os
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    """로그 레벨 정의"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"
    
    # 봇 특화 레벨
    BOT = "BOT"
    CMD = "CMD"
    API = "API"
    TASK = "TASK"
    PROCESS = "PROCESS"
    CONFIG = "CONFIG"
    DISCORD = "DISCORD"


class Colors:
    """ANSI 색상 코드"""
    # 기본 색상
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # 스타일
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    # 배경색 (선택사항)
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'


class Logger:
    """통합 로거 클래스"""
    
    # 로그 레벨별 색상 매핑
    LEVEL_COLORS = {
        LogLevel.DEBUG: Colors.GRAY,
        LogLevel.INFO: Colors.BLUE,
        LogLevel.WARN: Colors.YELLOW,
        LogLevel.ERROR: Colors.RED,
        LogLevel.FATAL: Colors.BG_RED + Colors.WHITE,
        
        # 봇 특화 색상
        LogLevel.BOT: Colors.GREEN,
        LogLevel.CMD: Colors.CYAN,
        LogLevel.API: Colors.MAGENTA,
        LogLevel.TASK: Colors.BLUE,
        LogLevel.PROCESS: Colors.YELLOW,
        LogLevel.CONFIG: Colors.CYAN,
        LogLevel.DISCORD: Colors.GREEN,
    }
    
    def __init__(self, enable_colors=None, enable_timestamp=True):
        """
        Args:
            enable_colors: 색상 활성화 여부 (None=자동감지, True=강제활성화, False=비활성화)
            enable_timestamp: 타임스탬프 포함 여부
        """
        # 색상 지원 자동 감지
        if enable_colors is None:
            # Windows CMD, PowerShell, Linux 터미널 등에서 색상 지원 확인
            self.enable_colors = (
                os.getenv('TERM') is not None or 
                os.getenv('ANSICON') is not None or
                'PYCHARM' in os.environ or
                'VSCODE' in os.environ.get('TERM_PROGRAM', '')
            )
        else:
            self.enable_colors = enable_colors
            
        self.enable_timestamp = enable_timestamp
    
    def _format_message(self, level: LogLevel, message: str) -> str:
        """메시지 포맷팅"""
        # 타임스탬프
        timestamp = ""
        if self.enable_timestamp:
            timestamp = f"{datetime.now().strftime('%H:%M:%S')} "
        
        # 색상 적용
        if self.enable_colors and level in self.LEVEL_COLORS:
            color = self.LEVEL_COLORS[level]
            level_str = f"{color}[{level.value}]{Colors.RESET}"
        else:
            level_str = f"[{level.value}]"
        
        return f"{timestamp}{level_str} {message}"
    
    def log(self, level: LogLevel, message: str):
        """기본 로그 함수"""
        formatted_message = self._format_message(level, message)
        print(formatted_message)
    
    # 편의 함수들
    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message: str):
        self.log(LogLevel.INFO, message)
    
    def warn(self, message: str):
        self.log(LogLevel.WARN, message)
    
    def error(self, message: str):
        self.log(LogLevel.ERROR, message)
    
    def fatal(self, message: str):
        self.log(LogLevel.FATAL, message)
    
    # 봇 특화 함수들
    def bot(self, message: str):
        self.log(LogLevel.BOT, message)
    
    def cmd(self, message: str):
        self.log(LogLevel.CMD, message)
    
    def api(self, message: str):
        self.log(LogLevel.API, message)
    
    def task(self, message: str):
        self.log(LogLevel.TASK, message)
    
    def process(self, message: str):
        self.log(LogLevel.PROCESS, message)
    
    def config(self, message: str):
        self.log(LogLevel.CONFIG, message)
    
    def discord(self, message: str):
        self.log(LogLevel.DISCORD, message)


# 전역 로거 인스턴스
logger = Logger()

# 편의를 위한 단축 함수들
def debug(message: str):
    logger.debug(message)

def info(message: str):
    logger.info(message)

def warn(message: str):
    logger.warn(message)

def error(message: str):
    logger.error(message)

def fatal(message: str):
    logger.fatal(message)

def bot(message: str):
    logger.bot(message)

def cmd(message: str):
    logger.cmd(message)

def api(message: str):
    logger.api(message)

def task(message: str):
    logger.task(message)

def process(message: str):
    logger.process(message)

def config(message: str):
    logger.config(message)

def discord(message: str):
    logger.discord(message)