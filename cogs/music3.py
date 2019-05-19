# -*- coding: utf-8 -*-

"""
The MIT License (MIT)
Copyright (c) 2019 apex2504
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


import logging
import math
import re
import discord
import datetime
import lavalink
from discord.ext import commands

time_rx = re.compile('[0-9]+')
url_rx = re.compile('https?:\/\/(?:www\.)?.+')  # noqa: W605

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.np=None

        if not hasattr(bot, 'lavalink'):
            lavalink.Client(bot=bot, password='youshallnotpass',
                            loop=bot.loop, log_level=logging.DEBUG)
            self.bot.lavalink.register_hook(self._track_hook)

    def cog_unload(self):
        for guild_id, player in self.bot.lavalink.players:
            self.bot.loop.create_task(player.disconnect())
            player.cleanup()

        # Clear the players from Lavalink's internal cache

        self.bot.lavalink.players.clear()
        self.bot.lavalink.unregister_hook(self._track_hook)

    async def _track_hook(self, event):
        if isinstance(event, lavalink.Events.StatsUpdateEvent):
            return

        channel = self.bot.get_channel(event.player.fetch('channel'))

        if not channel:
            return

        if isinstance(event, lavalink.Events.TrackStartEvent):
            requesterSong=await self.bot.fetch_user(int(event.track.requester))
            requesterName=requesterSong.name
            dur=None
            try:
                dur = str(datetime.timedelta(seconds=int(event.track.duration)/1000))
            except:
                dur="Livestream"
            if self.np:
                try:
                    await self.np.delete()
                except:
                    pass
            embed=discord.Embed(title="Now playing", description=f"{event.track.title}\nUploaded by {event.track.author}\nDuration: {dur}", color=65280)
            embed.set_footer(text=f"Requested by {requesterName}")
            embed.set_thumbnail(url=event.track.thumbnail)
            self.np=await channel.send(embed=embed)

        elif isinstance(event, lavalink.Events.QueueEndEvent):
            if self.np:
                try:
                    await self.np.delete()
                except:
                    pass
            await channel.send('Queue ended!')

    @commands.command(name='play', aliases=['p'])
    @commands.guild_only()
    async def _play(self, ctx, *, query: str):

        """ Searches and plays a song from a given query. """

        player = self.bot.lavalink.players.get(ctx.guild.id)
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=65280)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Added a playlist to the queue'
            embed.description = f'{results["playlistInfo"]["name"]} with {len(tracks)} songs'
            await ctx.send(embed=embed)

        else:
            track = results['tracks'][0]
            pos=None
            player = self.bot.lavalink.players.get(ctx.guild.id)
            if str(len(player.queue))=="0":
                pos="Next up"
            else:
                pos = str(len(player.queue))
            embed.title = 'Added to queue'
            dur=None
            try:
                dur = str(datetime.timedelta(seconds=int(track["info"]["length"])/1000))
            except:
                dur="Livestream"
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})\nUploaded by {track["info"]["author"]}\nDuration: {dur}\n\nPosition in queue: {pos}'
            #embed.set_thumbnail(url=f'{track["info"]["thumbnail"]}')
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)

            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

    @commands.command(name='previous', aliases=['pv', 'back'])
    @commands.guild_only()
    async def _previous(self, ctx):

        """ Plays the previous song. """

        player = self.bot.lavalink.players.get(ctx.guild.id)

        try:
            await player.play_previous()
        except lavalink.NoPreviousTrack:
            await ctx.send('There is no previous song to play.')

    @commands.command(name='playnow', aliases=['pn'])
    @commands.guild_only()
    async def _playnow(self, ctx, *, query: str):

        """ Plays immediately a song. """

        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not ctx.author.guild_permissions.kick_members:
            if ctx.author.id != int(player.current.requester):
                await ctx.send("You don't have permission to jump the queue")
                return

        if not player.queue and not player.is_playing:
            return await ctx.invoke(self._play, query=query)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        tracks = results['tracks']
        track = tracks.pop(0)

        if results['loadType'] == 'PLAYLIST_LOADED':
            for _track in tracks:
                player.add(requester=ctx.author.id, track=_track)

        await player.play_now(requester=ctx.author.id, track=track)

    @commands.command(name='playat', aliases=['pa'])
    @commands.guild_only()
    async def _playat(self, ctx, index: int):

        """ Plays the queue from a specific point. Disregards tracks before the index. """

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if index < 1:
            return await ctx.send('You can\'t do that')

        if len(player.queue) < index:
            return await ctx.send('The queue isn\'t that long')

        await player.play_at(index-1)

    @commands.command(name='seek')
    @commands.guild_only()
    async def _seek(self, ctx, *, time: str):

        """ Seeks to a given position in a track. """

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        seconds = time_rx.search(time)

        if not seconds:
            return await ctx.send('You need to specify the time to seek to')

        seconds = int(seconds.group()) * 1000
        track_time = seconds

        await player.seek(track_time)
        await ctx.send(f'Playing from **{lavalink.Utils.format_time(track_time)}**')

    @commands.command(name='skip', aliases=['forceskip', 'fs'])
    @commands.guild_only()
    async def _skip(self, ctx):

        """ Skips the current track. """

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not ctx.author.guild_permissions.kick_members:
            if ctx.author.id != int(player.current.requester):
                await ctx.send("You don't have permission to skip this song.")
                return

        if not player.is_playing:
            return await ctx.send('Not playing.')

        await player.skip()
        if self.np:
            try:
                await self.np.delete()
            except:
                pass

        await ctx.send('⏭')

    @commands.command(name='now', aliases=['np', 'n', 'playing'])
    @commands.guild_only()
    async def _now(self, ctx):

        """ Shows some stats about the currently playing song. """

        player = self.bot.lavalink.players.get(ctx.guild.id)

        song = 'Nothing'
        position=None

        if player.current:
            position = "Live"
            if player.current.stream:
                duration = 'Livestream'
            else:
                position = lavalink.Utils.format_time(player.position)
                duration = lavalink.Utils.format_time(player.current.duration)

            song = f'[{player.current.title}]({player.current.uri})\nUploaded by {player.current.author}\n`{position}/{duration}`'

        if self.np:
            try:
                await self.np.delete()
            except:
                pass
        embed = discord.Embed(color=65280,
                              title='Now Playing', description=song)
        requesterSong=await self.bot.fetch_user(int(player.current.requester))
        requesterName=requesterSong.name
        embed.set_footer(text=f"Requested by {requesterName}")
        embed.set_thumbnail(url=player.current.thumbnail)
        self.np=await ctx.send(embed=embed)

    @commands.command(name='queue', aliases=['q'])
    @commands.guild_only()
    async def _queue(self, ctx, page: int = 1):

        """ Shows the player's queue. """

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('There\'s nothing in the queue! Why not queue something?')

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        queue_list = ''

        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [{track.title}]({track.uri})\n'

        embed = discord.Embed(colour=65280,
                              description=f'{len(player.queue)} songs in the queue\n\n{queue_list}')
        embed.set_footer(text=f'Page {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(name='pause', aliases=['resume'])
    @commands.guild_only()
    async def _pause(self, ctx):

        """ Pauses/Resumes the current track. """

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing is playing right now')

        if ctx.author.guild_permissions.kick_members:
            if player.paused:
                await player.set_pause(False)
                return await ctx.send(":arrow_forward:")
            else:
                await player.set_pause(True)
                return await ctx.send(":pause_button:")

        if player.paused:
            if ctx.author.voice.channel.id == int(player.channel_id):
                VC= self.bot.get_channel(int(player.channel_id))
                isUserInVC=VC.members
                if len(isUserInVC)==2:
                    for VCmember in isUserInVC:
                        if VCmember.id==ctx.author.id:
                            await player.set_pause(False)
                            return await ctx.send(':arrow_forward:')
                else:
                    await ctx.send("You can't pause songs whilst other people are in the voice channel.")
            else:
                await ctx.send("We aren't in the same voice channel")

        else:
            if ctx.author.voice.channel.id == int(player.channel_id):
                VC= self.bot.get_channel(int(player.channel_id))
                isUserInVC=VC.members
                if len(isUserInVC)==2:
                    for VCmember in isUserInVC:
                        if VCmember.id==ctx.author.id:
                            await player.set_pause(True)
                            return await ctx.send(':pause_button:')
                else:
                    await ctx.send("You can't pause songs whilst other people are in the voice channel.")
            else:
                await ctx.send("We aren't in the same voice channel")

    @commands.command(name='volume', aliases=['vol'])
    @commands.guild_only()
    async def _volume(self, ctx, volume: int = None):

        """ Changes the player's volume. Must be between 0 and 1000. Error Handling for that is done by Lavalink. """
        await ctx.send("Changing volume has been disabled whilst we investigate issues causing the music to stop after changing volume\nWe apologise for any inconvenience caused.")
        return

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'🔈 {player.volume}%')

        if volume>200:
            return await ctx.send(f"{volume}% is too high")

        if volume<1:
            return await ctx.send(f"{volume}% is too low")

        await player.set_volume(volume)
        await ctx.send(f'🔈 Set to {player.volume}%')

    @commands.command(name='shuffle')
    @commands.guild_only()
    async def _shuffle(self, ctx):

        """ Shuffles the player's queue. """

        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("You don't have permission to shuffle the queue.")
            return

        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        player.shuffle = not player.shuffle
        await ctx.send('🔀 ' + ('Enabled' if player.shuffle else 'Disabled'))

    @commands.command(name='repeat', aliases=['loop'])
    @commands.guild_only()
    async def _repeat(self, ctx):

        """ Repeats the current song until the command is invoked again. """

        player = self.bot.lavalink.players.get(ctx.guild.id)
        if ctx.author.guild_permissions.kick_members:
            player.repeat = not player.repeat
            return await ctx.send('🔁 ' + ('Enabled' if player.repeat else 'Disabled'))

        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        if str(player.repeat)=="False":
            if ctx.author.voice.channel.id == int(player.channel_id):
                print(str(self))
                VC= self.bot.get_channel(int(player.channel_id))
                isUserInVC=VC.members
                if len(isUserInVC)==2:
                    for VCmember in isUserInVC:
                        if VCmember.id==ctx.author.id:
                            player.repeat = not player.repeat
                            return await ctx.send('🔁 ' + ('Enabled' if player.repeat else 'Disabled'))
                else:
                    await ctx.send("You can't repeat songs whilst other people are in the voice channel.")
            else:
                await ctx.send("We aren't in the same voice channel")
        else:
            if ctx.author.voice.channel.id == int(player.channel_id):
                VC= self.bot.get_channel(int(player.channel_id))
                isUserInVC=VC.members
                for VCmember in isUserInVC:
                    if VCmember.id==ctx.author.id:
                        player.repeat = not player.repeat
                        return await ctx.send('🔁 ' + ('Enabled' if player.repeat else 'Disabled'))
            else:
                await ctx.send("We aren't in the same voice channel")

    @commands.command(name='remove')
    @commands.guild_only()
    async def _remove(self, ctx, index: int):

        """ Removes an item from the player's queue with the given index. """

        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.queue:
            return await ctx.send('Nothing queued.')
        if index > len(player.queue) or index < 1:
            return await ctx.send(f'Number needs to be between 1 and {len(player.queue)}')
        index -= 1
        if not ctx.author.guild_permissions.kick_members:
            removeRequester=player.queue[index]
            if ctx.author.id != int(removeRequester.requester):
                await ctx.send("You don't have permission to remove songs from thr queue")
                return
        removed = player.queue.pop(index)
        await ctx.send(f'Removed **{removed.title}** from the queue.')

    @commands.command(name="move")
    @commands.guild_only()
    async def _move(self, ctx, original: int, new: int):
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if ctx.author.guild_permissions.kick_members:
            try:
                player.queue[original-1], player.queue[new-1] = player.queue[new-1], player.queue[original-1]
                await ctx.send(f"Moved {player.queue[new-1].title} to position `{new}` and moved {player.queue[original-1].title} to position `{original}`")
            except Exception as e:
                await ctx.send(f"""Couldn't move items```{e}```""")
                return
        else:
            await ctx.send("You don't have permission to reorder the queue")

    @commands.command(name='find', aliases=["search"])
    @commands.guild_only()
    async def _find(self, ctx, *, query):

        """ Lists the first 10 search results from a given query. """

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found')

        tracks = results['tracks'][:10]  # First 10 results

        o = ''

        for index, track in enumerate(tracks, start=1):
            track_title = track["info"]["title"]
            track_uri = track["info"]["uri"]
            o += f'`{index}.` [{track_title}]({track_uri})\n'

        embed = discord.Embed(color=65280, description=o)
        await ctx.send(embed=embed)

    @commands.command(name='disconnect', aliases=['dc', 'stop'])
    @commands.guild_only()
    async def _disconnect(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('I\'m not connected to a voice channel')

        if ctx.author.guild_permissions.kick_members:
            player.queue.clear()
            await player.stop()
            await player.disconnect()
            return await ctx.send(':stop_button:  Cleared the queue and disconnected from voice channel')

        if ctx.author.voice.channel.id == int(player.channel_id):
            VC= self.bot.get_channel(int(player.channel_id))
            isUserInVC=VC.members
            if len(isUserInVC)==2:
                for VCmember in isUserInVC:
                    if VCmember.id==ctx.author.id:
                        player.queue.clear()
                        await player.stop()
                        await player.disconnect()
                        await ctx.send(':stop_button:  Cleared the queue and disconnected from voice channel')

    @_playnow.before_invoke
    @_previous.before_invoke
    @_play.before_invoke
    async def ensure_voice(self, ctx):

        """ A few checks to make sure the bot can join a voice channel. """

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel:
                await ctx.send('You aren\'t connected to any voice channel.')
                raise commands.CommandInvokeError(
                    'Author not connected to voice channel.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                await ctx.send('Missing permissions `CONNECT` and/or `SPEAK`.')
                raise commands.CommandInvokeError(
                    'Bot has no permissions CONNECT and/or SPEAK')
            player.store('channel', ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)
        else:
            if player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send('Join my voice channel!')


def setup(bot):
    bot.add_cog(Music(bot))
