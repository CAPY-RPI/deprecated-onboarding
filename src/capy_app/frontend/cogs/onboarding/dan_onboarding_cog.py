import discord
import logging
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings
import random


class RandomCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(
            f"discord.cog.{self.__class__.__name__.lower()}"
        )

    @app_commands.guilds(discord.Object(id=settings.DEBUG_GUILD_ID))
    @app_commands.command(
        name="randomnum",
        description="Picks a random number between input lower and upper bounds"
    )
    async def randomnum(self,interaction: discord.Interaction, lower_bound: int, upper_bound: int):
        if lower_bound > upper_bound:
            message = "Lower bound must be <= Upper bound"
        else:
            message = f"{random.randint(lower_bound, upper_bound)} is your number"

        embed = discord.Embed(
            title="Random Number",
            description=message,
            color=colors.PING,
        )

        self.logger.info(message)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomCog(bot))
