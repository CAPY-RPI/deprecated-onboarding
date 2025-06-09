import discord
import logging
import asyncio
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings
import random



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
    
    async def arithmetic_game(self, interaction: discord.Interaction):
        # You can implement the game logic here
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(["+", "-", "*", "/"])

        challenge = f"What is {num1} {operation} {num2}?"
        await interaction.followup.send(challenge)
        
        if operation == '+':
            correct_answer = num1 + num2
        elif operation == '-':
            correct_answer = num1 - num2
        elif operation == '*':
            correct_answer = num1 * num2
        elif operation == '/':
            correct_answer = num1 / num2
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timed out! You took too long to answer.")
            return

        try:
            user_answer = float(msg.content)
        except ValueError:
            await interaction.followup.send("Invalid answer. Please enter a numeric value.")
            return

        if abs(user_answer - correct_answer) < 0.001:
            await interaction.followup.send("Correct!")
        else:
            await interaction.followup.send(f"Incorrect. The correct answer was {correct_answer}.")

        
async def setup(bot: commands.Bot):
    await bot.add_cog(SayedCog(bot))
