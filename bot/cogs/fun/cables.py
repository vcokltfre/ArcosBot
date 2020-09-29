import random
import discord
import os
from discord.ext import commands

from bot.bot import Bot

image_location = "/home/vcokltfre/Cables/"
images = [image_location + file for file in os.listdir(image_location)]


class CablePics(commands.Cog):
    """Get random images of nice cable management"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="cable", aliases=["cablepic"])
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def get_cable(self, ctx: commands.Context):
        """Get a random image of good cable management"""
        await ctx.send(file=discord.File(random.choice(images)))

    @get_cable.error
    async def cable_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("You are on cooldown, try again in a few seconds.", delete_after=10)
            return
        
        self.bot.logger.error(str(error))


def setup(bot: Bot):
    bot.add_cog(CablePics(bot))
