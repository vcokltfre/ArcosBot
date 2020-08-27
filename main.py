from discord.ext import commands

from bot.bot import run

cogs = [
    "utility.general",
    "core.status",
    "core.misc"

]

cogs = ["bot.cogs." + cog for cog in cogs]

run(cogs, prefix=["a?", "arcos "], help_command=commands.MinimalHelpCommand())