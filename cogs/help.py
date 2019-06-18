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


import discord
from discord.ext import commands
import asyncio
import json


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name="help", aliases=["commands"])
    async def help(self, ctx, request=None):
        if not request:
            with open("required files/prefixes.json", "r") as f:
                prefix=json.load(f)
            thisGuildPrefix=str(prefix[str(ctx.guild.id)]["prefix"].split())[1:-1]
            embed = discord.Embed(title='Help', description=f'<> indicates a required argument, [] indicates an optional argument.\nThis guild\'s prefixes are {thisGuildPrefix}', color=65280)
            embed.add_field(name='Utility', value="**help** - Shows this help message.\n**info** - Gives you info about Takagibot\n**serverinfo** - Gives you info about the server\n**userinfo [@member]** - Gives you info about your (or someone else's) Discord account\n**avatar [@member]** - Sends yours or someone else's avatar in the chat", inline=False)
            embed.add_field(name='Fun', value='**thank <@member>** - Very cool!\n**poll <"question"> <emojiOne> <emojiTwo>** - Creates a poll for others to vote on.\n**oopsie <@member>** - Someone did an oopsie!\n**subcount** - Shows you the number of subscribers for PewDiePie and T-Series and the difference between them.\n**dog** - Sends a random photo of a dog from the Dog API', inline=False)
            embed.add_field(name='Moderation', value='**kick <@member>** - Kicks a member from the server\n**ban <@member>** - Bans a member from the server.\n**mute <@member> [time]** - Mutes a member\n**unmute <@member>** - Unmutes a member\n**clear <number>** - Deletes a number of messages', inline=False)
            embed.add_field(name='Roles', value='**join <role name>** - Joins a role\n**leave <role name>** - Leaves a role\n**roles** - Shows you a list of assignable roles', inline=False)
            embed.add_field(name='Economy', value='**daily** - Get your daily credits\n**balance** - Check how many credits you have\n**shop [buy <number>]** - Shows the available items to buy, and allows you to buy them\n**gift <member> <amount>** - Gift people credits', inline=False)
            embed.add_field(name='Music', value='**play** - Plays music. You can search for a song, paste its link, or add a playlist\n**pause** - Pauses the music\n**resume** - Resumes music if it is paused.\n**stop** - Stops playing, clears the queue, and disconnects from the voice channel\n**skip** - Skip a song\n**prev** - Play again the previous song\n**queue [page number]** - Shows that queue page number\n**repeat** - Repeat a song or queue\n**playnow** - Plays a song straight away\n**shuffle** - Shuffles the queue\n**remove <number>** - Removes that numbered item from the queue\n**np** - Gets the info of the currently playing song\n**playat <number>** - Skips to that number in the queue\n**move <queue number> <queue number>** - Swaps the position of two songs in the queue\n**seek <seconds>** - Skips the specified number of seconds.\n**search <search string>** - Search YouTube for a song.', inline=False)
            embed.add_field(name='Levels', value='**rank [@member]** - Check the rank, level and XP of members.\n**top** - See the top 10 users in the server.', inline=False)
            embed.add_field(name='Configuration', value='**settings [part [value]]** - Shows you the available settings and allows you to change them', inline=False)
            embed.set_footer(text='Takagibot - Message @apex#2504 for help.')
            await ctx.send(embed=embed)
        elif request.lower()=="help":
            embed=discord.Embed(title="Help", description="This command shows you all commands or help for a particular command.", color=65280)
            embed.add_field(name="Aliases", value="help\ncommands", inline=False)
            embed.add_field(name="Usage", value="`help [optional command]`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="help":
            embed=discord.Embed(title="Info", description="This command shows you information about Takagibot.", color=65280)
            embed.add_field(name="Aliases", value="info", inline=False)
            embed.add_field(name="Usage", value="`info`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="serverinfo":
            embed=discord.Embed(title="Serverinfo", description="This command gives you useful information about the server.", color=65280)
            embed.add_field(name="Aliases", value="serverinfo\nguildinfo\nserver\nguild", inline=False)
            embed.add_field(name="Usage", value="`serverinfo`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="userinfo":
            embed=discord.Embed(title="Userinfo", description="This command gives you useful information about yourself or another user.", color=65280)
            embed.add_field(name="Aliases", value="userinfo\nuser", inline=False)
            embed.add_field(name="Usage", value="`userinfo [optional name/mention]`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="avatar":
            embed=discord.Embed(title="Help", description="This command sends your's or someone else's avatar in the chat.", color=65280)
            embed.add_field(name="Aliases", value="avatar\nprofilephoto\nphoto", inline=False)
            embed.add_field(name="Usage", value="`avatar [optional user]`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="thank":
            embed=discord.Embed(title="Thank", description="This command sends a Tweet from Donald Trump thanking the member.", color=65280)
            embed.add_field(name="Aliases", value="thank\nty", inline=False)
            embed.add_field(name="Usage", value="`thank [optional user]`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="poll":
            embed=discord.Embed(title="Help", description="This command creates a poll and allows users to vote on it.", color=65280)
            embed.add_field(name="Aliases", value="poll", inline=False)
            embed.add_field(name="Usage", value="`poll <'Question in quotes'> <First reaction> <Second reaction>`\nYou cannot use custom server emojis as reations.", inline=False)
            embed.add_field(name="Required permissions", value="Kick members", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="oopsie":
            embed=discord.Embed(title="Help", description="This command lets a user know that they did an oopsie!", color=65280)
            embed.add_field(name="Aliases", value="oopsie", inline=False)
            embed.add_field(name="Usage", value="`oopsie <required member>`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="subcount":
            embed=discord.Embed(title="Help", description="This command shows you the number of subscribers for PewDiePie and T-Series and the difference between them.", color=65280)
            embed.add_field(name="Aliases", value="subcount", inline=False)
            embed.add_field(name="Usage", value="`subcount`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="dog":
            embed=discord.Embed(title="Dog", description="This command sends a random photo of a dog from the Dog API.", color=65280)
            embed.add_field(name="Aliases", value="dog", inline=False)
            embed.add_field(name="Usage", value="`dog`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="giveaway":
            embed=discord.Embed(title="Giveaway", description="This command will start and automatically draw a giveaway after the given time.", color=65280)
            embed.add_field(name="Aliases", value="giveaway", inline=False)
            embed.add_field(name="Usage", value="`giveaway <required duration in days> <required prize>`", inline=False)
            embed.add_field(name="Required permissions", value="Administrator", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="kick":
            embed=discord.Embed(title="Kick", description="This command will kick a member from the server.", color=65280)
            embed.add_field(name="Aliases", value="kick", inline=False)
            embed.add_field(name="Usage", value="`kick <required @member>`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="ban":
            embed=discord.Embed(title="Ban", description="This command will ban a member from the server.", color=65280)
            embed.add_field(name="Aliases", value="ban", inline=False)
            embed.add_field(name="Usage", value="`ban <required @member>`", inline=False)
            embed.add_field(name="Required permissions", value="Ban members", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="mute":
            embed=discord.Embed(title="Mute", description="This command will mute a member (stopping them from typing or speaking in a voice channel).", color=65280)
            embed.add_field(name="Aliases", value="mute", inline=False)
            embed.add_field(name="Usage", value="`mute <@member> [optional time e.g. 10m]`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="unmute":
            embed=discord.Embed(title="Unmute", description="This command will unmute a member (allow them to type and speak again).", color=65280)
            embed.add_field(name="Aliases", value="unmute", inline=False)
            embed.add_field(name="Usage", value="`unmute <required @member>`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="clear":
            embed=discord.Embed(title="Clear", description="This command will clear the specified number of messages (excluding the command message).", color=65280)
            embed.add_field(name="Aliases", value="clear\npurge", inline=False)
            embed.add_field(name="Usage", value="`clear <required number>`", inline=False)
            embed.add_field(name="Required permissions", value="Manage messages", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="join":
            embed=discord.Embed(title="Join", description="This command allows you to join a role.", color=65280)
            embed.add_field(name="Aliases", value="join\nrole\njoinrole", inline=False)
            embed.add_field(name="Usage", value="`join <required role name>`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="leave":
            embed=discord.Embed(title="Clear", description="This command allows you to leave a role.", color=65280)
            embed.add_field(name="Aliases", value="leave\leaverole", inline=False)
            embed.add_field(name="Usage", value="`leave <required role name>`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="roles":
            embed=discord.Embed(title="Roles", description="This command will show you all the roles you can join.", color=65280)
            embed.add_field(name="Aliases", value="roles\nranks", inline=False)
            embed.add_field(name="Usage", value="`roles`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="daily":
            embed=discord.Embed(title="Daily", description="This command gives you your 10 daily credits. You can only run this command once a day, resetting at midnight UTC", color=65280)
            embed.add_field(name="Aliases", value="daily", inline=False)
            embed.add_field(name="Usage", value="`daily`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="gift":
            embed=discord.Embed(title="Gift", description="This command will give the specified member the specified number of credits (providing you have enough).", color=65280)
            embed.add_field(name="Aliases", value="gift\ngive", inline=False)
            embed.add_field(name="Usage", value="`gift <required member> <required number of credits>`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="rank":
            embed=discord.Embed(title="Rank", description="This command shows you your rank on the leaderboard, as well as your XP and level. You can also get the rank of another member.", color=65280)
            embed.add_field(name="Aliases", value="rank\nlevel", inline=False)
            embed.add_field(name="Usage", value="`rank [optional member]`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="top":
            embed=discord.Embed(title="Top", description="This command shows you the top 10 most active members in the server, as well as your position in the leaderboard.", color=65280)
            embed.add_field(name="Aliases", value="top\nleaderboard", inline=False)
            embed.add_field(name="Usage", value="`top`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="play":
            embed=discord.Embed(title="Play", description="This command will play a song in your current voice channel. It will add to the queue if there is already another song playing.", color=65280)
            embed.add_field(name="Aliases", value="play\np", inline=False)
            embed.add_field(name="Usage", value="`play <required song name/link>`", inline=False)
            embed.add_field(name="Required permissions", value="None", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="skip":
            embed=discord.Embed(title="Skip", description="This command will skip the currently playing song.", color=65280)
            embed.add_field(name="Aliases", value="skip\ns\nforceskip", inline=False)
            embed.add_field(name="Usage", value="`skip`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="pause":
            embed=discord.Embed(title="Pause", description="This command pauses the currently playing song.", color=65280)
            embed.add_field(name="Aliases", value="pause\nresume", inline=False)
            embed.add_field(name="Usage", value="`pause`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="resume":
            embed=discord.Embed(title="Resume", description="This command resumes the currently playing song.", color=65280)
            embed.add_field(name="Aliases", value="resume\npause", inline=False)
            embed.add_field(name="Usage", value="`resume`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="playnow":
            embed=discord.Embed(title="Playnow", description="This command plays a song straight away, disregarding the current song.", color=65280)
            embed.add_field(name="Aliases", value="playnow", inline=False)
            embed.add_field(name="Usage", value="`playnow <required song name/link>`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="playat":
            embed=discord.Embed(title="Playat", description="This command will start playaing from the given queue position, disregarding any songs before it.", color=65280)
            embed.add_field(name="Aliases", value="playat", inline=False)
            embed.add_field(name="Usage", value="`playat <required queue position>`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="Prev":
            embed=discord.Embed(title="Prev", description="This command plays again the previous song.", color=65280)
            embed.add_field(name="Aliases", value="prev\nback\nprevious", inline=False)
            embed.add_field(name="Usage", value="`prev`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="shuffle":
            embed=discord.Embed(title="Shuffle", description="This command shuffles the queue.", color=65280)
            embed.add_field(name="Aliases", value="shuffle", inline=False)
            embed.add_field(name="Usage", value="`shuffle`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="repeat":
            embed=discord.Embed(title="Repeat", description="This command will cuse the bot to repeat the queue.", color=65280)
            embed.add_field(name="Aliases", value="repeat\nloop", inline=False)
            embed.add_field(name="Usage", value="`repeat`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="move":
            embed=discord.Embed(title="Move", description="This command moves the specified song to a new specified position in the queue", color=65280)
            embed.add_field(name="Aliases", value="move", inline=False)
            embed.add_field(name="Usage", value="`move <required original position> <required new position>`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="remove":
            embed=discord.Embed(title="Remove", description="This command removes the song in the given position from the queue.", color=65280)
            embed.add_field(name="Aliases", value="remove", inline=False)
            embed.add_field(name="Usage", value="`remove <required queue number>`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="stop":
            embed=discord.Embed(title="Stop", description="This command will clear the queue and disconnect from the voice channel.", color=65280)
            embed.add_field(name="Aliases", value="stop\ndisconnect\ndc", inline=False)
            embed.add_field(name="Usage", value="`stop`", inline=False)
            embed.add_field(name="Required permissions", value="Kick members (being alone with the bot also works)", inline=False)
            await ctx.send(embed=embed)
        elif request.lower()=="settings":
            embed=discord.Embed(title="Settings", description="This command shows you the bot's settings page", color=65280)
            embed.add_field(name="Aliases", value="settings\nset", inline=False)
            embed.add_field(name="Usage", value="`settings [optional part [optional new value]]`", inline=False)
            embed.add_field(name="Required permissions", value="Administrator (being the bot owner also works)", inline=False)
            await ctx.send(embed=embed)
        else:
            return await ctx.send("That isn't a valid command. Use **help** to see whats available")



def setup(bot):
    bot.add_cog(Help(bot))
