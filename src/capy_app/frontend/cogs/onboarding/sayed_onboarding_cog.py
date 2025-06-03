import discord
import logging
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings
import asyncio


class SayedCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(
            f"discord.cog.{self.__class__.__name__.lower()}"
        )

    @app_commands.guilds(discord.Object(id=settings.DEBUG_GUILD_ID))
    @app_commands.command(name="countdown", description="Counts down the input seconds to 0. Allowed range is 1-30 seconds.")
    async def countdown(self, interaction: discord.Interaction, seconds: int):
        if seconds < 1 or seconds > 30:
            await interaction.response.send_message(
                "Please provide a number between 1 and 30 seconds.",
                ephemeral=True,
            )
            return
        await interaction.response.send_message(
            f"Counting down from {seconds} seconds...",
            ephemeral=True,
        )
        
        for i in range(seconds, 0, -1):
            await asyncio.sleep(1)
            await interaction.edit_original_response(content=f"{i}...")
        await asyncio.sleep(1)
        await interaction.edit_original_response(content="Time's up!")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(SayedCog(bot))
