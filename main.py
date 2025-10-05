import discord
import signal
import sys
import os
import atexit

from discord.ext import commands
from core.config import Config
from core.exceptions import ConfigurationError
from cogs.recommender_cog import RecommenderCog
from cogs.tag_cog import TagCog
from utils.logger import info, process, warn, error


# PID 파일 경로
PID_FILE = 'bot.pid'

def create_pid_file():
    """
    📌 PID 파일 생성으로 중복 실행을 방지
    """
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            old_pid = f.read().strip()
        
        # 기존 프로세스가 실제로 실행 중인지 확인
        try:
            os.kill(int(old_pid), 0)
            warn(f"봇이 이미 실행 중입니다 (PID: {old_pid})")
            warn("기존 봇을 종료하고 다시 시도하세요.")
            sys.exit(1)
        except (OSError, ValueError):
            # 프로세스가 존재하지 않으면 PID 파일 삭제
            os.remove(PID_FILE)
    
    # 새 PID 파일 생성
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    process(f"PID 파일 생성됨: {os.getpid()}")

def cleanup():
    """
    📌 정리 작업을 수행 (PID 파일 삭제)
    """
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
        process("PID 파일 삭제됨")

def signal_handler(signum, frame):
    """
    📌 시그널 핸들러를 정의 (graceful shutdown)
    """
    process(f"시그널 {signum} 수신됨. 봇을 안전하게 종료합니다.")
    cleanup()
    sys.exit(0)

# 시그널 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # 프로세스 종료

# 프로그램 종료 시 정리 작업 등록
atexit.register(cleanup)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)



"""
📌 메인 함수 정의
"""
def main():
    try:
        # 1. 설정 인스턴스 생성 (환경변수 검증 포함)
        config = Config()
        info("환경변수 설정을 로드하였습니다.")

        # 2. Discord Bot 인스턴스 생성
        intents = discord.Intents.all()
        bot = commands.Bot(command_prefix='!', intents=intents)

        # 3. Bot 이벤트 등록
        @bot.event
        async def on_ready():
            info(f"{bot.user.name}으로 로그인되었습니다. (ID: {bot.user.id})")

            # TODO: 나중에 컨테이너 패턴으로 변경 예정
            await bot.add_cog(RecommenderCog(bot))
            await bot.add_cog(TagCog(bot))

        # 4. PID 파일 생성 및 봇 실행
        create_pid_file()
        info("Discord Bot을 시작합니다.")
        info("종료하려면 Ctrl+C를 누르세요.")

        # 5. 설정에서 토큰 가져오기
        bot.run(config.get_discord_token())

    except ConfigurationError as e:
        error(f"설정 오류: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        process("KeyboardInterrupt 감지됨. 봇을 종료합니다.")
    except Exception as e:
        error(f"예상치 못한 오류: {e}")
        sys.exit(1)
    finally:
        cleanup()
        info("봇이 완전히 종료되었습니다.")

if __name__ == "__main__":
    main()