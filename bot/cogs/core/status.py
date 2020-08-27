import json
import discord
from discord.ext import commands, tasks
from pathlib import Path
from random import choice

from bot.bot import Bot
from bot.utils.checks import is_dev


class Status(commands.Cog):
    """Dynamically change the bot's status during operation"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.enabled = True
        self.statuses = []
        self.load_statuses()

    def load_statuses(self):
        with Path("./bot/static/statuses.json").open() as f:
            data = json.load(f)
        self.statuses = data

    async def set_status(self, status):
        await self.bot.change_presence(activity=discord.Game(name=status))

    @commands.group(name="status")
    @is_dev()
    async def status_group(self, ctx: commands.Context):
        """A command group for controlling Arcos' status"""
        if ctx.invoked_subcommand == None:
            await ctx.send("Invalid usage. Please use `a?help status` for help with this command.")

    @status_group.command(name="set")
    async def status_set(self, ctx: commands.Context, *status):
        """Set the status manually"""
        status = " ".join(status)
        await self.set_status(status)
        self.enabled = False
        await ctx.send(f"Set the status to `{status}`")

    @status_group.command(name="enable", aliases=["reset", "start"])
    async def status_enable(self, ctx: commands.Context):
        """Enable automatic status updates"""
        self.enabled = True
        await ctx.send("Enabled automatic status updates.")

    @status_group.command(name="disable", aliases=["stop"])
    async def status_enable(self, ctx: commands.Context):
        """Disable automatic status updates"""
        self.enabled = False
        await ctx.send("Disabled automatic status updates.")

    @commands.Cog.listener()
    async def on_ready(self):
        self.status_loop.start()
        self.bot.logger.info("Arcos has started")
        self.bot.logger.info("Starting automatic status updates")

    @tasks.loop(seconds=60)
    async def status_loop(self):
        if self.enabled:
            await self.set_status(choice(self.statuses))


def setup(bot: Bot):
    bot.add_cog(Status(bot))