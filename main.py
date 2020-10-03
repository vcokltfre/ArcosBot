from discord.ext import commands

from bot.bot import run

cogs = [
    "utility.general",
    "utility.charinfo",
    "core.status",
    "core.misc",
    "core.config",
    "fun.catpics",
    "fun.dogpics",
    "fun.cables",
    "fun.stickbug"
]

cogs = ["bot.cogs." + cog for cog in cogs]
cogs.append("jishaku")

run(cogs, help_command=commands.MinimalHelpCommand())