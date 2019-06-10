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
"""
This Music cog is based on the Lavalink.py v3 example. This re-introduces a few features that were taken out of v3 and an extra event.
Like the rest of Takagibot, this requires Python 3.6 or above.
"""
import math
import re
import discord
import lavalink
from discord.ext import commands

url_rx = re.compile('https?:\\/\\/(?:www\\.)?.+')  # noqa: W605


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.np=None
        self.channel=None

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('127.0.0.1', 2333, 'youshallnotpass', 'eu', 'default-node')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        bot.lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            if self.np:
                try:
                    await self.np.delete()
                except:
                    pass
            await self.channel.send('Queue ended!')
        if isinstance(event, lavalink.events.TrackStartEvent):
            requesterSong=await self.bot.fetch_user(int(event.track.requester))
            requesterName=requesterSong.name
            dur=None
            try:
                dur = lavalink.utils.format_time(event.track.duration)
            except:
                dur="Livestream"
            if self.np:
                try:
                    await self.np.delete()
                except:
                    pass
            embed=discord.Embed(title="Now playing", description=f"{event.track.title}\nUploaded by {event.track.author}\nDuration: {dur}", color=65280)
            embed.set_footer(text=f"Requested by {requesterName}")
            embed.set_thumbnail(url=f"http://i3.ytimg.com/vi/{event.track.identifier}/hqdefault.jpg")
            self.np=await self.channel.send(embed=embed)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=65280)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Added a playlist to the queue'
            embed.description = f'{results["playlistInfo"]["name"]} with {len(tracks)} songs'
        else:
            track = results['tracks'][0]
            pos=None
            if str(len(player.queue))=="0":
                pos="Next up"
            else:
                pos = str(len(player.queue))
            dur=None
            try:
                dur = lavalink.utils.format_time(track["info"]["length"])
            except:
                dur="Livestream"
            embed.title = 'Added to queue'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})\nUploaded by {track["info"]["author"]}\nDuration: {dur}'
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            embed.set_thumbnail(url=f'http://i3.ytimg.com/vi/{track["info"]["identifier"]}/hqdefault.jpg')
            player.add(requester=ctx.author.id, track=track)
        self.channel=ctx.channel
        await ctx.send(embed=embed)

        if not player.is_playing:
            await player.play()

    @commands.command(name="playnow")
    async def playnow(self, ctx, *, query:str):
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
        else:
            player.add(requester=ctx.author.id, track=track)
            player.queue.insert(0, player.queue.pop(len(player.queue)-1))

        if player.shuffle:
            player.shuffle=not player.shuffle
            await player.stop()
            await player.play()
            player.shuffle=not player.shuffle
        else:
            await player.stop()
            await player.play()


    @commands.command(name="playat")
    async def playat(self, ctx, index:int):
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not ctx.author.guild_permissions.kick_members:
            if ctx.author.voice.channel.id != int(player.channel_id):
                return await ctx.send("We aren't in the same voice channel!")
            VC= self.bot.get_channel(int(player.channel_id))
            isUserInVC=VC.members
            if len(isUserInVC)==2:
                if index>len(player.queue)+1:
                    return await ctx.send("The queue isn't that long!")
                else:
                    for i in range(index-1):
                        del player.queue[0]
            else:
                return await ctx.send("You can't jump the queue while other people are in the voice channel.")
        else:
            if index>len(player.queue)+1:
                return await ctx.send("The queue isn't that long!")
            else:
                for i in range(index-1):
                    del player.queue[0]
        if player.shuffle:
            player.shuffle=not player.shuffle
            await player.stop()
            await player.play()
            player.shuffle=not player.shuffle
        else:
            await player.stop()
            await player.play()



    @commands.command()
    async def seek(self, ctx, *, seconds: int):
        """ Seeks to a given position in a track. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        if not seconds:
            return await ctx.send('You need to specify the time to seek to')
        track_time = seconds * 1000
        await player.seek(track_time)
        await ctx.send(f'Moved track to **{lavalink.utils.format_time(track_time)}**')

    @commands.command(aliases=['forceskip', 's'])
    async def skip(self, ctx):
        """ Skips the current track. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not ctx.author.guild_permissions.kick_members:
            if ctx.author.id != int(player.current.requester):
                await ctx.send("You don't have permission to skip this song.")
                return

        if not player.is_playing:
            return await ctx.send('Nothing is playing right now!')

        await player.skip()
        await ctx.send('⏭')

    @commands.command(aliases=['np', 'n', 'playing'])
    async def now(self, ctx):
        """ Shows some stats about the currently playing song. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.current:
            return await ctx.send('Nothing playing.')

        position="Livestream"
        duration="Livestream"
        if not player.current.stream:
            position = lavalink.utils.format_time(player.position)
            duration = lavalink.utils.format_time(player.current.duration)

        song = f'[{player.current.title}]({player.current.uri})\nUploaded by {player.current.author}\n`{position}/{duration}`'

        embed = discord.Embed(color=65280,
                              title='Now Playing', description=song)
        requesterSong=await self.bot.fetch_user(int(player.current.requester))
        requesterName=requesterSong.name
        embed.set_footer(text=f"Requested by {requesterName}")
        embed.set_thumbnail(url=f"http://i3.ytimg.com/vi/{player.current.identifier}/hqdefault.jpg")
        self.np=await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int = 1):
        """ Shows the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('Nothing queued.')

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=65280, title=f"{len(player.queue)} songs in the queue",
                              description=f'{queue_list}')
        embed.set_footer(text=f'Page {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
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

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int = None):
        """ Changes the player's volume (0-200). """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not ctx.author.guild_permissions.kick_members:
            return await ctx.send("Only a moderator can change the volume")

        if not volume:
            return await ctx.send(f'🔈 | {player.volume}%')

        if volume > 200:
            return await ctx.send(f"{volume}% is too high")
        elif volume <1:
            return await ctx.send(f"{volume}% is too low")

        await player.set_volume(volume)
        await ctx.send(f'🔈 | Set to {player.volume}%')

    @commands.command()
    async def shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        if ctx.author.guild_permissions.kick_members:
            player.shuffle = not player.shuffle
            await ctx.send('🔀 ' + ('Enabled' if player.shuffle else 'Disabled'))

        if str(player.shuffle)=="False":
            if ctx.author.voice.channel.id == int(player.channel_id):
                print(str(self))
                VC= self.bot.get_channel(int(player.channel_id))
                isUserInVC=VC.members
                if len(isUserInVC)==2:
                    for VCmember in isUserInVC:
                        if VCmember.id==ctx.author.id:
                            player.shuffle = not player.shuffle
                            return await ctx.send('🔀 ' + ('Enabled' if player.shuffle else 'Disabled'))
                else:
                    await ctx.send("You can't shuffle songs whilst other people are in the voice channel.")
            else:
                await ctx.send("We aren't in the same voice channel")
        else:
            if ctx.author.voice.channel.id == int(player.channel_id):
                VC= self.bot.get_channel(int(player.channel_id))
                isUserInVC=VC.members
                for VCmember in isUserInVC:
                    if VCmember.id==ctx.author.id:
                        player.shuffle = not player.shuffle
                        return await ctx.send('🔀 ' + ('Enabled' if player.shuffle else 'Disabled'))
            else:
                await ctx.send("We aren't in the same voice channel")

    @commands.command(aliases=['loop'])
    async def repeat(self, ctx):
        """ Repeats the current song until the command is invoked again. """
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        if ctx.author.guild_permissions.kick_members:
            player.repeat = not player.repeat
            return await ctx.send('🔁 ' + ('Enabled' if player.repeat else 'Disabled'))


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

    @commands.command()
    async def remove(self, ctx, index: int):
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
    async def move(self, ctx, original:int=None, new:int=None):
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if ctx.author.guild_permissions.kick_members:
            try:
                original-=1
                new-=1
                player.queue.insert(new, player.queue.pop(original))
                await ctx.send(f"Moved {player.queue[new].title} to position {new+1}")
            except Exception as e:
                await ctx.send(f"""Couldn't move items```{e}```""")
                return

    @commands.command()
    async def search(self, ctx, *, query):
        """ Lists the first 10 search results from a given query. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found.')

        tracks = results['tracks'][:10]  # First 10 results

        o = ''
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            o += f'`{index}.` [{track_title}]({track_uri})\n'

        embed = discord.Embed(color=65280, description=o)
        await ctx.send(embed=embed)

    @commands.command(aliases=['stop', 'dc'])
    async def disconnect(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('I\'m not connected to a voice channel')

        if ctx.author.guild_permissions.kick_members:
            player.queue.clear()
            await player.stop()
            await self.connect_to(ctx.guild.id, None)
            return await ctx.send(':stop_button:  Cleared the queue and disconnected from voice channel')

        if ctx.author.voice.channel.id == int(player.channel_id):
            VC= self.bot.get_channel(int(player.channel_id))
            isUserInVC=VC.members
            if len(isUserInVC)==2:
                for VCmember in isUserInVC:
                    if VCmember.id==ctx.author.id:
                        player.queue.clear()
                        await player.stop()
                        await self.connect_to(ctx.guild.id, None)
                        await ctx.send(':stop_button:  Cleared the queue and disconnected from voice channel')


    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.players.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.

        should_connect = ctx.command.name in ('play')  # Add commands that require joining voice to work.

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')

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


def setup(bot):
    bot.add_cog(Music(bot))
