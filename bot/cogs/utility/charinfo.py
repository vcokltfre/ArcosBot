import requests
import discord
from discord.ext import commands

from bot.bot import Bot
from unicodedata import name


class CharInfo(commands.Cog):
    """Get info for characters"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="chars")
    async def get_cat(self, ctx: commands.Context, *, data: str):
        """Get char info for a sequence of chars"""
        text = "```css\n"
        for letter in data:
            text += f"{ord(letter)}: {name(letter)}\n"
        await ctx.send(text + "```")


def setup(bot: Bot):
    bot.add_cog(CharInfo(bot))
