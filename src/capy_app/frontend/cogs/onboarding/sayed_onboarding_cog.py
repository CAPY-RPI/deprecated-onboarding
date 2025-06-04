import discord
import logging
import asyncio
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings



class SayedCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(
            f"discord.cog.{self.__class__.__name__.lower()}"
        )

    @app_commands.guilds(discord.Object(id=settings.DEBUG_GUILD_ID))
    @app_commands.command(name="countdown", description="Counts down the input seconds to 0. Allowed range is 1-30 seconds.")
    async def countdown(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 1, 30]):
        # Defer the response to avoid a timeout
        await interaction.response.defer()

        try:
            await interaction.edit_original_response(content=f"Counting down from {seconds} seconds...")
        except discord.HTTPException as e:
            self.logger.error(f"Failed to edit initial response: {e}")
        for i in range(seconds, 0, -1):
            await asyncio.sleep(1)
            try:
                await interaction.edit_original_response(content=f"{i}...")
            except discord.HTTPException as e:
                self.logger.error(f"Failed to edit countdown response at {i}: {e}")
        await asyncio.sleep(1)
        try:
            await interaction.edit_original_response(content="Time's up!")
        except discord.HTTPException as e:
            self.logger.error(f"Failed to edit final response: {e}")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(SayedCog(bot))
