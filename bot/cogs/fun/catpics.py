import requests
import discord
from discord.ext import commands

from bot.bot import Bot
from config.config import cat_token

api_location = "https://api.thecatapi.com/v1/images/search"


class CatPics(commands.Cog):
    """Get random images of cats"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="cat", aliases=["catpic"])
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def get_cat(self, ctx: commands.Context):
        """Get a random image of a cat"""
        response = requests.get(api_location, headers={"x-api-token": cat_token})
        cat_url = response.json()[0]["url"]
        await ctx.channel.send(cat_url)

    @get_cat.error
    async def cat_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send("You are on cooldown, try again in a few seconds.", delete_after=10)
            return
        
        self.bot.logger.error(str(error))


def setup(bot: Bot):
    bot.add_cog(CatPics(bot))