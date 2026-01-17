import atexit
import os
import signal
import sys

import discord
from discord.ext import commands

from algomori.core.config import Config
from algomori.core.exceptions import ConfigurationError
from algomori.core.guild_config_store import GuildConfigStore
from algomori.discord.cogs.recommender_cog import RecommenderCog
from algomori.discord.cogs.settings_cog import SettingsCog
from algomori.discord.cogs.tag_cog import TagCog
from algomori.services.api_client import SolvedAcClient
from algomori.services.problem_service import ProblemService
from algomori.utils.logger import info, process, warn, error


PID_FILE = "bot.pid"


def create_pid_file() -> None:
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r", encoding="utf-8") as f:
            old_pid = f.read().strip()

        try:
            os.kill(int(old_pid), 0)
            warn(f"봇이 이미 실행 중입니다 (PID: {old_pid})")
            warn("기존 봇을 종료하고 다시 시도하세요.")
            raise SystemExit(1)
        except (OSError, ValueError):
            os.remove(PID_FILE)

    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))

    process(f"PID 파일 생성됨: {os.getpid()}")


def cleanup() -> None:
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
        process("PID 파일 삭제됨")


def _signal_handler(signum, frame) -> None:
    process(f"시그널 {signum} 수신됨. 봇을 안전하게 종료합니다.")
    cleanup()
    raise SystemExit(0)


def create_bot(config: Config) -> commands.Bot:
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    api_client = SolvedAcClient()
    problem_service = ProblemService(api_client)
    config_store = GuildConfigStore(file_path=config.get_guild_config_path())

    @bot.event
    async def on_ready():
        info(f"{bot.user.name}으로 로그인되었습니다. (ID: {bot.user.id})")

        await bot.add_cog(RecommenderCog(bot, problem_service=problem_service, config_store=config_store))
        await bot.add_cog(TagCog(bot))
        await bot.add_cog(SettingsCog(bot, config_store=config_store))

    return bot


def run() -> None:
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    atexit.register(cleanup)

    try:
        config = Config()
        info("환경변수 설정을 로드하였습니다.")

        bot = create_bot(config)

        create_pid_file()
        info("Discord Bot을 시작합니다.")
        info("종료하려면 Ctrl+C를 누르세요.")

        bot.run(config.get_discord_token())

    except ConfigurationError as e:
        error(f"설정 오류: {e}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        process("KeyboardInterrupt 감지됨. 봇을 종료합니다.")
    except SystemExit:
        raise
    except Exception as e:
        error(f"예상치 못한 오류: {e}")
        raise SystemExit(1)
    finally:
        cleanup()
        info("봇이 완전히 종료되었습니다.")
