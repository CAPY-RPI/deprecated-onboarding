import discord
import logging
import random
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings


class ThomasCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(
            f"discord.cog.{self.__class__.__name__.lower()}"
        )
        
        self.random_lines = [
            "Every good thing that happens to you in this game is preplanned like a show. There's an audience waiting for your downfall."
            "...I should buy a boat."
            "So... come here often?"
            "Wanna hear a joke?"
            "Im out of funny ideas, come back later"
            "Check out this cool gif"
            "I'm hungry. Like, I really could go for some rigatoni right now."
            "I've been thinking of starting a band recently. Might call it [adjective] [noun]. What do you think?"
        ]
        
        self.random_images = [
            "https://tenor.com/view/destroyman-destroyman-iii-destroyman-3-deepwoken-deepwoken-destroyman-gif-7822491813183790485"
            "https://tenor.com/view/destroyman-destroyman-iii-destroyman-3-deepwoken-deepwoken-destroyman-gif-241781888877782845"
            "https://media.discordapp.net/attachments/820192358158172160/1099738116329320598/EF5CD357-44D9-4097-8F3F-E67BF676FEA2.gif?ex=6840786f&is=683f26ef&hm=b2436104426390d1b0d2bbef8b5ac9a9e6db345e21a13a2059787a0db5a250d0&"
            "https://tenor.com/view/gullible-gif-23847583"
            "https://tenor.com/view/petting-aligator-crocodile-gif-25954785"
            "https://tenor.com/view/obama-ballin-basketball-gif-19387821"
        ]

    @app_commands.guilds(discord.Object(id=settings.DEBUG_GUILD_ID))
    @app_commands.command(name="thomas", description="Does Something")
    async def Thomas(self, interaction: discord.Interaction):
        line = random.choice(self.random_lines)
        image = random.choice(self.random_images)
        
        embed = discord.Embed(
            title="Tom",
            description=line,
            color=colors.PING,
        )
        embed.set_image(url=image)
        
        self.logger.info(f"Selected line: {line}, image: {image}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ThomasCog(bot))
