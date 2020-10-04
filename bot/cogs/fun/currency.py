import json
import discord
from discord.ext import commands

from bot.bot import Bot
from bot.utils.checks import is_dev


class Currency(commands.Cog):
    """Administrator currency commands for Arcos"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(name="currency")
    @is_dev()
    async def currency(self, ctx: commands.Context):
        """Administrator currency commands for Arcos"""
        if ctx.invoked_subcommand == None:
            pass

    @currency.command(name="set")
    async def curr_set(self, ctx: commands.Context, amount: int, member: str = None):
        if not member:
            member = str(ctx.author.id)
        mdata = self.bot.api.get_by_uid("users", "user_id", member)
        self.bot.logger.info(f"Currency SET: Data: {mdata}")
        cdata = {"balance": amount}
        if mdata and "currency" in mdata:
            cdata = mdata["currency"]
            cdata["balance"] = amount
        self.bot.api.update("users", "user_id", member, {"currency": cdata})
        await ctx.send(f"Balance for {member} has been set to {amount}")

    @currency.command(name="get")
    async def curr_get(self, ctx: commands.Context, member: str = None):
        if not member:
            member = str(ctx.author.id)
        mdata = self.bot.api.get_by_uid("users", "user_id", member)
        if not mdata or not "currency" in mdata:
            await ctx.send("There is no currency data for this user")
            return
        cdata = mdata["currency"]
        await ctx.send(f"Balance for {member}: {cdata['balance']}")


def setup(bot: Bot):
    bot.add_cog(Currency(bot))