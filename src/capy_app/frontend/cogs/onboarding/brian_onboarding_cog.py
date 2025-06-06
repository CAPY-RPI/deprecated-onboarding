import discord
import logging
from discord.ext import commands
from discord import app_commands

from frontend import config_colors as colors
from config import settings


class todoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(
            f"discord.cog.{self.__class__.__name__.lower()}"
        )
        self.todolists = {}  # Dictionary to hold todo lists for each user
        self.message_tracker = {} # Dictionary to track messages for each user


    @app_commands.guilds(discord.Object(id=settings.DEBUG_GUILD_ID))
    @app_commands.command(name="todo", description="creates todo list")
    async def todo(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        task_list = self.todolists.get(user_id, [])
        description_dynamic = "\n".join(task_list) if task_list else "No tasks in your todo list."
        embed = discord.Embed(
            title = f"{interaction.user.name}'s Todo List",
            description = description_dynamic,
            color = colors.TODO,
        )
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()

        self.message_tracker[user_id] = message.id  # Track the message ID for the user

        #reaction buttons
        await message.add_reaction("➕")
        await message.add_reaction("❌")
        await message.add_reaction("✅")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Ignore bot reactions
        if user.bot:
            return  

        # Check if the reaction is on a tracked message
        message = reaction.message
        if message not in self.tracked_messages:
            return
        
        user_id = self.tracked_messages[message.id]
        if user.id != user_id:
            await message.channel.send(f"{user.mention}, you can only manage your own todo list.", delete_after=5)
            return

        if reaction.emoji == "➕":
            await self.add_task(reaction.message, user)
        elif reaction.emoji == "❌":
            await self.remove_task(reaction.message, user)
        elif reaction.emoji == "✅":
            await self.close_task_list(reaction.message, user)

    async def add_task(self, message, user):
        await message.channel.send(f"{user.mention}, what task would you like to add?", delete_after=10)

        def check(m):
            return m.author == user and m.channel == message.channel

        try:
            reply = await self.bot.wait_for("message", check=check, timeout=30.0)
            task = reply.content.strip()
            if task:
                self.todolists.setdefault(user.id, []).append(task)
                await self.update_embed(message, user.id)
        except Exception:
            await message.channel.send(f"{user.mention}, task add timed out or failed.", delete_after=5)
        
    async def remove_task(self, message, user):
        await message.channel.send(f"{user.mention}, this feature is not implemented yet.", delete_after=5)
    async def close_task_list(self, message, user):
        await message.channel.send(f"{user.mention}, this feature is not implemented yet.", delete_after=5)

    async def update_embed(self, message, user_id):
        task_list = self.todolists.get(user_id, [])
        new_description = "\n".join(task_list) if task_list else "No tasks in your todo list."

        embed = message.embeds[0]
        embed.description = new_description
        await message.edit(embed=embed)
async def setup(bot: commands.Bot):
    await bot.add_cog(todoCog(bot))