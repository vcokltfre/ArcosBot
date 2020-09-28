import json
import discord
from discord.ext import commands
from pathlib import Path

from bot.bot import Bot
from bot.utils.checks import is_dev

symbol = "1234567890!\"£$%^&*()[]{};#':~@,./<>?\\|`¬ "
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
valid = alpha + symbol


class Config(commands.Cog):
    """Customizability for Arcos"""

    def __init__(self, bot: Bot):
        self.bot = bot

    def validate_prefix(self, prefix: str):
        if 1 > len(prefix) or len(prefix) > 8:
            return False
        for letter in prefix:
            if not letter in valid:
                return False
        return True

    @commands.group(name="config")
    @commands.check_any(commands.has_permissions(manage_guild=True), is_dev())
    async def config_group(self, ctx: commands.Context):
        """Change Arcos config options"""
        if ctx.invoked_subcommand == None:
            pass

    @config_group.command(name="prefix")
    async def cfg_prefix(self, ctx: commands.Context, *, prefix: str = None):
        """View or change your guild prefix"""
        gid = str(ctx.guild.id)
        if not prefix:
            pref = "a?"
            if gid in self.bot.prefixes:
                pref = self.bot.prefixes[gid]
            await ctx.channel.send(f"Your prefix for Arcos is `{pref}`")
        else:
            if self.validate_prefix(prefix):
                self.bot.api.update("guilds", "guild_id", gid, {"prefix": prefix})
                self.bot.prefixes[gid] = prefix
                await ctx.channel.send(f"Your new prefix for Arcos is `{prefix}`")
            else:
                await ctx.channel.send("Your prefix must contain only ASCII characters and be between 1 and 8 characters long.")


def setup(bot: Bot):
    bot.add_cog(Config(bot))