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
    @app_commands.command(name="poll", description="Shows the bot's latency")
    async def poll(self, interaction: discord.Interaction, question: str, choice1: str, choice2: str, choice3: str = None):
        choices = [choice1, choice2]
        if choice3:
            choices.append(choice3)
        emojis = ["1️⃣", "2️⃣", "3️⃣"]
        
        
        descriptions = []                           #to describe each choice
        for i, choice in enumerate(choices):        #enumerate gives index & choice text while looping through choices
            descrip = f"{emojis[i]} {choice}"       #combine emoji (number) + choice 
            descriptions.append(descrip)            #add line to descriptions
        
        
        message = f"⏱ {round(self.bot.latency * 1000)} ms Latency!"
        embed = discord.Embed(
            title="Poll",
            description=message,
            color=colors.POLL,  #renamed PING to POLL ... idk if i was supposed to do this
        )
        self.logger.info(message)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(KayleeCog(bot))
