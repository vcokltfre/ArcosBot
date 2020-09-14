import requests
import discord
from discord.ext import commands

from bot.bot import Bot

api_location = "https://dog.ceo/api/breeds/image/random"


class DogPics(commands.Cog):
    """Get random images of dogs"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="dog", aliases=["dogpic"])
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def get_dog(self, ctx: commands.Context):
        """Get a random image of a dog"""
        response = requests.get(api_location)
        dog_url = response.json()["message"]
        await ctx.channel.send(dog_url)

    @get_dog.error
    async def dog_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send("You are on cooldown, try again in a few seconds.", delete_after=10)
            return

        self.bot.logger.error(str(error))


def setup(bot: Bot):
    bot.add_cog(DogPics(bot))