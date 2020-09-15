from discord.ext import commands

from bot.bot import run

cogs = [
    "utility.general",
    "core.status",
    "core.misc",
    "core.config",
    "fun.catpics",
    "fun.dogpics",
    "jishaku"
]

cogs = ["bot.cogs." + cog for cog in cogs]

run(cogs, help_command=commands.MinimalHelpCommand())