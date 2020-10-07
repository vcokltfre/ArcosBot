# -*- coding: utf-8 -*-

from discord.ext import commands
from datetime import timedelta
import discord
import lavalink
import re

from config.config import ll_region, ll_port, ll_host, ll_node, ll_pass

url_rx = re.compile(r'https?://(?:www\.)?.+')

def mb(memory: int):
    return f"{memory // (1024*1024)}MB"


class Music(commands.Cog):
    """A music cog for Arcos"""

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(689160870143590621)
            bot.lavalink.add_node(ll_host, ll_port, ll_pass, ll_region, ll_node)
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink_event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))

        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('You must be in a voice channel!')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    ## COMMANDS

    @commands.command(name="play", aliases = ["p", "pl"])
    async def play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('No results matched your query.')

        embed = discord.Embed(color=discord.Color.blurple())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for i, track in enumerate(tracks):
                player.add(requester=ctx.author.id, track=track)

                if i == 10:
                    break

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        if not player.is_playing:
            await player.play()

    @commands.command(name="disconnect", aliases=['d', 'dc', 'stop'])
    async def disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Not connected, can\'t disconnect.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!')

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | Disconnected.')

    @commands.command(name="vcns")
    @commands.is_owner()
    async def nodestats(self, ctx):
        node = self.bot.lavalink.node_manager.nodes[0]
        stats = node.stats

        e = discord.Embed(title="Lavalink Node Statistics", description=f"Uptime: {str(timedelta(milliseconds=stats.uptime)).split('.')[0]}", color=discord.Colour.blurple())
        e.add_field(name="Memory (Used / Free / Allocated / Reservable)", value=f"{mb(stats.memory_used)} / {mb(stats.memory_free)} / {mb(stats.memory_allocated)} / {mb(stats.memory_reservable)}", inline=False)
        e.add_field(name="Connected Players", value=str(stats.players))
        e.add_field(name="Active Players", value=str(stats.playing_players))
        e.add_field(name="Cores", value=str(stats.cpu_cores))
        e.add_field(name="System Load", value=str(stats.system_load))
        e.add_field(name="Lavalink Load", value=str(stats.lavalink_load))
        e.add_field(name="Frames Sent / Nulled", value=f"{stats.frames_sent} / {stats.frames_nulled}")

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Music(bot))
