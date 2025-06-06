import discord
import logging
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings
import random

class EliasCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(
            f"discord.cog.{self.__class__.__name__.lower()}"
        )
        self.status_emojis = {
            "🪨": "Rock",
            "🧻": "Paper",
            "✂️": "Scissors",
        }
          
    @app_commands.guilds(discord.Object(id=settings.DEBUG_GUILD_ID))
    @app_commands.command(name="rps", description="Plays Rock Paper Scissors with the bot!", )
    async def rps(self, interaction: discord.Interaction):
        
        message = f"React to play!"
        self.logger.info(message)
        embed = discord.Embed(
            title="Rock Paper Scissors",
            description=message,
            color=colors.GUILD,
        )
        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        for emoji in self.status_emojis.keys():
                await msg.add_reaction(emoji)
        self.bot.rps_message_id = msg.id
        self.bot.rps_user_id = interaction.user.id

    def determine_winner(self, user_choice: str, bot_choice: str) -> str:
        if user_choice == bot_choice:
            return "tied"
        wins_against = {
            "Rock": "Scissors",
            "Scissors": "Paper",
            "Paper": "Rock",
        }
        if wins_against[user_choice] == bot_choice:
            return "won ⭐"
        else:
            return "lost ❌"
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return

        if not hasattr(self.bot, "rps_message_id") or reaction.message.id != self.bot.rps_message_id:
            return

        if user.id != self.bot.rps_user_id:
            return

        choice = self.status_emojis.get(str(reaction.emoji))
        if not choice:
            return
        # Delete reaction version
        await reaction.message.clear_reactions()
        
        #Delete message version
        #wait reaction.message.delete()

        # Choose bot's random move
        import random
        bot_choice = random.choice(["Rock", "Paper", "Scissors"])
        result = self.determine_winner(choice, bot_choice)

        await reaction.message.channel.send(
            f"{user.mention} chose **{choice}**, I chose **{bot_choice}**. You **{result}**!"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(EliasCog(bot))
