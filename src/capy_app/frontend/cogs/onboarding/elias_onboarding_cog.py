import discord
import logging
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings


class EliasCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(
            f"discord.cog.{self.__class__.__name__.lower()}"
        )
        self.status_emojis = {
            "🪨": "Rock",
            "": "Paper",
            "✂️": "Scissors",
            "⭐": "Won",
            "❌": "Lost",
        }
    @app_commands.guilds(discord.Object(id=settings.DEBUG_GUILD_ID))
    @app_commands.command(name="RPS", description="Plays Rock Paper Scissors with the bot!", )
    async def ping(self, interaction: discord.Interaction, arg1):
        for emoji in self.status_emojis.keys():
                await message.add_reaction(emoji)
        message = f"Choose your reaction"
        embed = discord.Embed(
            title="Ping",
            description=message,
            color=colors.PING,
        )
        self.logger.info(message)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(EliasCog(bot))
