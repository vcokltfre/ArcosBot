from discord.ext import commands

from bot.bot import run

cogs = [
    "bot.cogs.utility.general",
    "bot.cogs.core.status"
]

run(cogs, prefix=["a?", "arcos "], help_command=commands.MinimalHelpCommand())