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
import datetime
import time
from pathlib import Path
from subprocess import Popen
from requests import get
from os.path import basename
from os.path import join
import os
import json

startTime=datetime.datetime.utcnow()

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    @commands.command(name='help')
    async def help(self, ctx, part=None):
        if (not part):
            with open("required files/prefixes.json", "r") as f:
                prefix=json.load(f)
            thisGuildPrefix=str(prefix[str(ctx.guild.id)]["prefix"].split())[1:-1]
            embed = discord.Embed(title='Help', description=f'<> indicates a required argument, [] indicates an optional argument.\nThis guild\'s prefixes are {thisGuildPrefix}', color=65280)
            embed.add_field(name='Utility', value="**help** - Shows this help message.\n**info** - Gives you info about Takagibot\n**serverinfo** - Gives you info about the server\n**userinfo [@member]** - Gives you info about your (or someone else's) Discord account.", inline=False)
            embed.add_field(name='Fun', value='**thank <@member>** - Very cool!\n**poll <"question"> <emojiOne> <emojiTwo>** - Creates a poll for others to vote on.\n**oopsie <@member>** - Someone did an oopsie!\n**subcount** - Shows you the number of subscribers for PewDiePie and T-Series and the difference between them.\n**dog** - Sends a random photo of a dog from the Dog API', inline=False)
            embed.add_field(name='Moderation', value='**kick <@member>** - Kicks a member from the server\n**ban <@member>** - Bans a member from the server.\n**mute <@member> [time]** - Mutes a member\n**unmute <@member>** - Unmutes a member\n**clear <number>** - Deletes a number of messages', inline=False)
            embed.add_field(name='Roles', value='**join <role name>** - Joins a role\n**leave <role name>** - Leaves a role\n**roles** - Shows you a list of assignable roles', inline=False)
            embed.add_field(name='Economy', value='**daily** - Get your daily credits\n**balance** - Check how many credits you have\n**shop [buy <number>]** - Shows the available items to buy, and allows you to buy them\n**gift <member> <amount>** - Gift people credits', inline=False)
            embed.add_field(name='Music', value='**play** - Plays music. You can search for a song, paste its link, or add a playlist\n**pause** - Pauses the music\n**resume** - Resumes music if it is paused.\n**stop** - Stops playing, clears the queue, and disconnects from the voice channel\n**skip** - Skip a song\n**queue [page number]** - Shows that queue page number\n**repeat** - Repeat a song or queue\n**playnow** - Plays a song straight away\n**shuffle** - Shuffles the queue\n**remove <number>** - Removes that numbered item from the queue\n**np** - Gets the info of the currently playing song\n**playat <number>** - Skips to that number in the queue\n**move <queue number> <queue number>** - Swaps the position of two songs in the queue\n**seek <seconds>** - Skips the specified number of seconds.\n**back** - Plays again the previous song\n**search <search string>** - Search YouTube for a song.', inline=False)
            embed.add_field(name='Levels', value='**rank [@member]** - Check the rank, level and XP of members.\n**top** - See the top 10 users in the server.', inline=False)
            embed.add_field(name='Configuration', value='**settings [part [value]]** - Shows you the available settings and allows you to change them', inline=False)
            embed.set_footer(text='Takagibot - Message @apex#2504 for help.')
            await ctx.send(embed=embed)
        elif part.lower() == 'utility':
            embed = discord.Embed(title='Help', description='These are commands that give you information on the bot or how to use it.', color=65280)
            embed.add_field(name='Utility', value='**help** - Shows this help message.\n**info** - Gives you info about Takagibot\n**serverinfo** - Gives you info about the server\n**userinfo [@member]** - Gives you info about a Discord account. To check info for someone else, type their name in the command.', inline=False)
            await ctx.send(embed=embed)
        elif part.lower() == 'fun':
            embed = discord.Embed(title='Help', description='These are fun commands that exist for entertainment. If you want something to be added, ping @apex#2504', color=65280)
            embed.add_field(name='Fun', value='**thank <@member>** - Thanks a member in a very cool way!\n**poll <"question"> <emojiOne> <emojiTwo>** - Creates a poll for others to vote on. The question MUST be in quotes. Example: poll "This is a question" :smile: :slight_frown:\n**oopsie <@member>** - Someone did an oopsie!\n**subcount** - Shows you the number of subscribers for PewDiePie and T-Series and the difference between them.\n**dog** - Sends a random photo of a dog from the Dog API', inline=False)
            await ctx.send(embed=embed)
        elif part.lower() == 'moderation':
            embed = discord.Embed(title='Help', description='These are commands that are only available to the mods. They are designed to help keep the server and its rules in place.', color=65280)
            embed.add_field(name='Moderation', value='**kick <@member>** - Kicks a member from the server. Member is a required field.\n**ban <@member>** - Bans a member from the server. Member is a required field.\n**mute <@member> [time]** - Mutes a member. Member is a required field. If no time is given, they will remain muted until you unmute them.\n**unmute <@member>** - Unmutes a member. Member is a required field.\n**clear <number>** - Deletes a number of messages. Number is a required field.', inline=False)
            await ctx.send(embed=embed)
        elif part.lower() == 'roles':
            embed = discord.Embed(title='Help', description='These commands are for the role system. Having a role allows you to have a nice colour and will allow you to enter role-only giveaways.', color=65280)
            embed.add_field(name='Roles', value='**join <role name>** - Joins a role. Name is a required field.\n**leave <role name>** - Leaves a role. Name is a required field.\n**roles** - Gives you a list of assignable roles', inline=False)
            await ctx.send(embed=embed)
        elif part.lower() == 'economy':
            embed = discord.Embed(title='Help', description='These are for the economy system', color=65280)
            embed.add_field(name='Economy', value='**daily** - Get your daily credits. This command can only be run once a day\n**balance** - Checks how many credits you have.\n**shop [buy <number>]** - Shows the available items to buy, and allows you to buy them\n**gift <member> <amount>** - Gift people credits. You can either ping someone or type their exact name. Both the member and amount are required fields.', inline=False)
            await ctx.send(embed=embed)
        elif part.lower() == 'music':
            embed = discord.Embed(title='Help', description='These commands are for controlling the music.', color=65280)
            embed.add_field(name='Music', value='**play** <search/link> - Plays music. You can search for a song, paste its link, or add a playlist\n**pause** - Pauses the music\n**resume** - Resumes music if it is paused.\n**stop** - Stops playing, clears the queue and leaves the voice channel\n**skip** - Skip a song\n**queue [page number]** - Shows that queue page number\n**repeat** - Repeat a song or queue\n**playnow** - Plays a song straight away\n**shuffle** - Shuffles the queue\n**remove <number>** - Removes that numbered item from the queue\n**np** - Gets the info of the currently playing song\n**playat <number>** - Skips to that number in the queue\n**move <queue number> <queue number>** - Swaps the positions of two songs in the queue\n**seek <seconds>** - Skips the specified number of seconds\n**back** - Plays again the previous song\n**search <search string>** - Search YouTube for a song.', inline=False)
            await ctx.send(embed=embed)
        elif part.lower() == 'levels':
            embed = discord.Embed(title='Help', description='These commands are for the TakagiBot levelling system..', color=65280)
            embed.add_field(name='Levels', value='**rank [member]** - Check your rank, level and XP. You can check the rank, level and XP of another member if you type their name.\n**top** - See the top 10 users in the server.', inline=False)
            await ctx.send(embed=embed)
        elif part.lower()=="configuration":
            embed=discord.Embed(title="Help", description="These allow you to change my settings. All settings require admin permissions")
            embed.add_field(name='Configuration', value='Use **<prefix>settings** to view available settings', inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="That isn't a valid category.", color=65280)
            embed.add_field(name='Available categories', value='Utility\nFun\nModeration\nRoles\nEconomy\nMusic\nLevels', inline=False)
            await ctx.send(embed=embed)
    @commands.command(name='serverinfo')
    async def guildinfo(self, ctx):
        allMembers = set(ctx.guild.members)
        offline = filter((lambda m: (m.status is discord.Status.offline)), allMembers)
        offline = set(offline)
        online = allMembers - offline
        botUsers = filter((lambda m: m.bot), allMembers)
        botUsers = set(botUsers)
        netUsers = allMembers - botUsers
        servericon = ctx.guild.icon_url
        server_passed = (ctx.message.created_at - ctx.guild.created_at).days
        server_created_at = "Created on {}\nThat's {} days ago!".format(ctx.guild.created_at.strftime('%d %b %Y %H:%M'), server_passed)
        embed = discord.Embed(title='Server info', color=65280)
        TextChannelNumber = 0
        VoiceChannelNumber = 0
        Categories = 0
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                TextChannelNumber+=1
            elif isinstance(channel, discord.VoiceChannel):
                VoiceChannelNumber+=1
            else:
                Categories += 1
        embed.add_field(name='Server', value=server_created_at, inline=False)
        embed.add_field(name='Channels', value=((((((str(Categories) + ' Categories\n') + str(TextChannelNumber)) + ' Text channels\n') + str(VoiceChannelNumber)) + ' Voice channels\n') + str(TextChannelNumber + VoiceChannelNumber)) + ' Total channels', inline=False)
        embed.add_field(name='Members', value='{0} total members\n{1} online members\n{2} offline members\n{3} humans\n{4} bots'.format(len(allMembers), len(online), len(offline), len(netUsers), len(botUsers)), inline=False)
        embed.add_field(name='Ownership', value=f'Owned by {ctx.guild.owner}', inline=False)
        embed.set_thumbnail(url=servericon)
        embed.set_footer(text='Server ID: ' + str(ctx.guild.id))
        await ctx.send(embed=embed)

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, userStats=None):
        if (not userStats):
            userStatus = ctx.author.status
            UserIcon = ctx.author.avatar_url
            AccountCreated = ctx.author.created_at.strftime('%d %b %Y %H:%M')
            account_passed = (ctx.message.created_at - ctx.author.created_at).days
            joinedAt = ctx.author.joined_at.strftime('%d %b %Y %H:%M')
            joined_passed = (ctx.message.created_at - ctx.author.joined_at).days
            embed = discord.Embed(title='User info for {}'.format(ctx.author.name), color=65280)
            embed.add_field(name='Basic', value="Currently in {} status\nAccount created on {}\nThat's {} days ago!".format(userStatus, AccountCreated, account_passed), inline=False)
            embed.add_field(name='Server', value="Joined server on the {}\nThat's {} days ago!".format(joinedAt, joined_passed), inline=False)
            rolesMsg = ''
            for role in ctx.author.roles:
                rolesMsg += str(role) + ', '
            embed.add_field(name='Roles', value=rolesMsg, inline=False)
            embed.set_thumbnail(url=UserIcon)
            embed.set_footer(text='User ID: ' + str(ctx.author.id))
            await ctx.send(embed=embed)
        else:
            if len(userStats)<3:
                await ctx.send("That name is too short. Try mentioning them instead.")
                return
            try:
                found=await self.bot.fetch_user(int(str(userStats)[2:-1]))
                userStatsPing=found.name
                for person in ctx.guild.members:
                    if userStatsPing.lower() in str(person).lower():
                        userStatus = person.status
                        UserIcon = person.avatar_url
                        AccountCreated = person.created_at.strftime('%d %b %Y %H:%M')
                        account_passed = (ctx.message.created_at - person.created_at).days
                        joinedAt = person.joined_at.strftime('%d %b %Y %H:%M')
                        joined_passed = (ctx.message.created_at - person.joined_at).days
                        embed = discord.Embed(title='User info for {}'.format(person.name), color=65280)
                        embed.add_field(name='Basic', value="Currently in {} status\nAccount created on {}\nThat's {} days ago!".format(userStatus, AccountCreated, account_passed), inline=False)
                        embed.add_field(name='Server', value="Joined server on the {}\nThat's {} days ago!".format(joinedAt, joined_passed), inline=False)
                        rolesMsg = ''
                        for role in person.roles:
                            rolesMsg += str(role) + ', '
                        embed.add_field(name='Roles', value=rolesMsg, inline=False)
                        embed.set_thumbnail(url=UserIcon)
                        embed.set_footer(text='User ID: ' + str(person.id))
                        await ctx.send(embed=embed)
                        return
            except:
                for person in ctx.guild.members:
                    if userStats.lower() in str(person).lower():
                        userStatus = person.status
                        UserIcon = person.avatar_url
                        AccountCreated = person.created_at.strftime('%d %b %Y %H:%M')
                        account_passed = (ctx.message.created_at - person.created_at).days
                        joinedAt = person.joined_at.strftime('%d %b %Y %H:%M')
                        joined_passed = (ctx.message.created_at - person.joined_at).days
                        embed = discord.Embed(title='User info for {}'.format(person.name), color=65280)
                        embed.add_field(name='Basic', value="Currently in {} status\nAccount created on {}\nThat's {} days ago!".format(userStatus, AccountCreated, account_passed), inline=False)
                        embed.add_field(name='Server', value="Joined server on the {}\nThat's {} days ago!".format(joinedAt, joined_passed), inline=False)
                        rolesMsg = ''
                        for role in person.roles:
                            rolesMsg += str(role) + ', '
                        embed.add_field(name='Roles', value=rolesMsg, inline=False)
                        embed.set_thumbnail(url=UserIcon)
                        embed.set_footer(text='User ID: ' + str(person.id))
                        await ctx.send(embed=embed)
                        return
                await ctx.send("There was a problem getting the info for that user.")

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        await ctx.send('There was a problem getting the info for that user')

    startTime=datetime.datetime.utcnow()



    @commands.command(name='info')
    async def info(self, ctx):
        timeNow = datetime.datetime.utcnow()
        diff = timeNow - startTime
        (hours, remainder) = divmod(int(diff.total_seconds()), 3600)
        (minutes, seconds) = divmod(remainder, 60)
        (days, hours) = divmod(hours, 24)
        if days:
            timeFormat = '{d} days, {h} hours, {m} minutes and {s} seconds'
        else:
            timeFormat = '{h} hours, {m} minutes and {s} seconds'
        uptimeStamp = timeFormat.format(d=days, h=hours, m=minutes, s=seconds)
        embed = discord.Embed(color=65280)
        embed.add_field(name='Info', value=f'Takagibot, created by **apex#2504**\nWritten in Python 3.6.8 using discord.py 1.0.0\nCurrently serving {len(self.bot.guilds)} guilds with {len(set(self.bot.get_all_members()))} total members\n\nUptime: {uptimeStamp}\nLatency: {round(self.bot.latency * 1000)}ms', inline=False)
        embed.add_field(name="Support", value="[Join my support server here](https://discord.gg/BRmPxbE)", inline=False)
        embed.add_field(name='Changelog\nLatest version: `1.3.5`', value="• Doggos!\n• Code cleanups. Might make getting your rank faster", inline=False)
        await ctx.send(embed=embed)


    @commands.command(name='restart')
    async def restart(self, ctx):
        if await ctx.bot.is_owner(ctx.author):
            await ctx.send("Restarting...")
            bot_folder=Path('*YOUR BOT FOLDER*')
            bot_file=bot_folder / "*YOUR BOT FILE.py*"
            Popen("python "+str(bot_file))
            quit()
        else:
            await ctx.send("Only the bot owner can restart me.")


def setup(bot):
    bot.add_cog(Utility(bot))
