import json
import discord
from discord.ext import commands
from pathlib import Path

from bot.bot import Bot
from bot.utils.checks import is_dev


class Misc(commands.Cog):
    """Miscellaneous commands for Arcos"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="credits")
    async def credits(self, ctx: commands.Context):
        with Path("./bot/static/credits.json").open() as f:
            data = json.load(f)

        desc = ""
        for key in data:
            desc += f"**{key}**: {data[key]['info']}\n"

        embed = discord.Embed(title="Arcos Cedits", description=desc, color=0x8FFF3F)
        await ctx.send(embed=embed)

    @commands.command(name="mimic")
    @is_dev()
    async def mimic(self, ctx: commands.Context, member: discord.Member, *, text):
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=str(member.nick if member.nick else member.name))
        await webhook.send(content=text, avatar_url=str(member.avatar_url))
        await webhook.delete()


def setup(bot: Bot):
    bot.add_cog(Misc(bot))