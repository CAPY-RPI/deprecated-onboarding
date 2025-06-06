import discord
import logging
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings

#change everything with "Ping"
class KayleeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(
            f"discord.cog.{self.__class__.__name__.lower()}"
        )

    @app_commands.guilds(discord.Object(id=settings.DEBUG_GUILD_ID))
    @app_commands.command(name="poll", description="Custom poll with 3 choices")
    async def poll(self, interaction: discord.Interaction, question: str, choice_1: str, choice_2: str, choice_3: str):
        choices = [choice_1, choice_2, choice_3]
        emojis = ["1️⃣", "2️⃣", "3️⃣"]
        
        #description string creation
        descriptions = []
        for i in range(3):
            descrip = emojis[i] + " " + choices[i]
            descriptions.append(descrip)
        message = "\n".join(descriptions)           #combine all into one string

        
        #description embed
        embed = discord.Embed(
            title = "Poll: " + question,
            description = message,
            #color = colors.POLL,       #couldn't get it to work :( gave me errors
        )
        self.logger.info(message)                               #logs message
        await interaction.response.send_message(embed=embed)    #replies to command with the embed

        #adding emoji reactions for voting
        msg = await interaction.original_response()     #get the reply message
        for i in range(3):
            await msg.add_reaction(emojis[i])           #reacts to that msg with each emoji


async def setup(bot: commands.Bot):
    await bot.add_cog(KayleeCog(bot))
