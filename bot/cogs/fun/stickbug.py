import discord
import requests
from discord.ext import commands

class stickbug(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stickbug", aliases=["sb"])
    async def stickbug(self, ctx, user: discord.User):
        """ Stickbuggs people with stickb.ug """
        url = f"https://stickb.ug/api/d/idavid/{user.id}/{user.avatar}"
        m = await ctx.send("wip")
        try:
            r = requests.get(url, timeout=15)
        except requests.exceptions.ReadTimeout:
            await m.edit(content="stickb.ug took too to long try it again later!")
            return
        if r.status_code == 429:
            await m.edit(content="Stick bug site is currently rate limited!\nTry again later!", delete_after=20)
            return
        elif r.status_code == 404:
            await m.edit(content="PFP not found! Or stickb.ug messed up!", delete_after=30)
            return
        elif r.status_code != 200:
            await m.edit(content="stickb.ug messed up!\n"+str(r.json()), delete_after=30)
            return
        await m.edit(content=f"done, `{user}` got stickbugged:\n{r.json().get('outputurl')}")

def setup(bot):
	bot.add_cog(stickbug(bot))