from discord.ext import commands

from bot.bot import run

cogs = [
    "utility.general",
    "core.status",
    "core.misc",
    "core.config",
    "fun.catpics",
    "fun.dogpics"
]

cogs = ["bot.cogs." + cog for cog in cogs]
cogs.append("jishaku")

run(cogs, help_command=commands.MinimalHelpCommand())