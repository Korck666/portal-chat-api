from typing import List
# import discord
from multiprocessing import Process
from utils.config import Config
from services.logger import Logger
from fastapi_discord import DiscordOAuthClient, RateLimited, Unauthorized, User
from fastapi_discord.exceptions import ClientSessionNotInitialized
from fastapi_discord.models import GuildPreview


config = Config()
logger = Logger()


class DiscordBot:
    _discord: DiscordOAuthClient
    _instance = None

    async def __new__(cls) -> "DiscordBot":
        """
        Singleton implementation for class DiscordBot.
        """
        if not cls._instance:
            cls._discord = DiscordOAuthClient(
                "<client-id>", "<client-secret>", "<redirect-url>", ("identify", "guilds", "email"))
            cls._instance = super().__new__(cls)
            await cls._instance._initialize()
            cls._process = Process(target=cls._run)
        return cls._instance

    async def _initialize(self):
        super().__init__()

        await self._discord.init()

        self._instance = self

@DiscordBot._discord.user
async def on_ready():
    logger.info(f'{self.client.user} has connected to Discord!')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:  # ignore messages from self
                return

            if message.content.startswith('!hello'):
                await message.channel.send('Hello!')

    @classmethod
    async def stop(cls):
        await cls._instance.client.close() if cls._instance else None
        cls._instance = None

    @classmethod
    async def _run(cls):
        cls._instance.client.run(config.DISCORD_APP_AUTH_TOKEN,
                                 reconnect=True,
                                 log_handler=logger.dbhandler) if cls._instance else None

    @classmethod
    def start(cls):
        cls._process.start()
