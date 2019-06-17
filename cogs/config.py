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
import json
import asyncio

with open("required files/prefixes.json") as f:
    prefixes = json.load(f)

def prefix(bot, message):
    id = message.guild.id
    guildPrefix=prefixes[str(message.guild.id)]["prefix"].split()
    return prefixes[str(message.guild.id)]["prefix"].split()

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    with open("required files/prefixes.json") as f:
        prefixes = json.load(f)

    def prefix(bot, message):
        id = message.guild.id
        guildPrefix=prefixes[str(message.guild.id)]["prefix"].split()
        return prefixes[str(message.guild.id)]["prefix"].split()

    @commands.command(name="settings", aliases=["setting", "set"])
    async def settings(self, ctx, setting=None, *, value:str=None):
        if not setting:
            embed=discord.Embed(title="Settings", description="If you just want to view the setting, you don't need to specify a value.\n<> denotes a required argument. [] denotes an optional argument.\nFor example:  **t!settings welcome** will show you the welcome channel.", color=65280)
            embed.add_field(name="Changing settings", value="""**welcome [channel name]** - Sets or shows you the welcome channel.
**rules [channel name]** - Sets or shows you the rules channel.
**levelup [channel name]** - Sets or shows you the level up channel.
**noxp [channel name]** - Sets or shows you the channels in which messages will not gain XP.
**gainxp <channel name>** - Allows a channel to gain XP again.
**addrole <role name>** - Allows a role to be self-assignable.
**removerole <role name>** - Stops a role from being self-assignable.
**prefix [values separated by a space]** - Sets or shows you this guild's prefixes.

Channel names do not require the # but do require the -'s if there are any.
Role names must be exact when adding them, but do not need to be exact when joining or leaving them.""", inline=False)
            embed.set_footer(text="Takagibot - written by apex#2504")
            return await ctx.send(embed=embed)
        elif setting.lower()=="prefix":
            with open('required files/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            if not await ctx.bot.is_owner(ctx.author):
                if not ctx.author.guild_permissions.administrator:
                    return await ctx.send(f"This guild's prefix is `{prefixes[str(ctx.guild.id)]['prefix'].split()}`")
                else:
                    if not value:
                        return await ctx.send(f"This guild's prefixes are `{prefixes[str(ctx.guild.id)]['prefix'].split()}`")
                    else:
                        if (not (str(ctx.guild.id) in prefixes)):
                            prefixes[str(ctx.guild.id)] = {

                            }
                            prefixes[str(ctx.guild.id)]['prefix'] = "t! T! t. T."
                            with open('required files/prefixes.json', 'w') as f:
                                json.dump(prefixes, f)
                        with open('required files/prefixes.json', 'r') as f:
                            prefixes[str(ctx.guild.id)]['prefix'] = str(value)
                        with open('required files/prefixes.json', 'w') as f:
                            json.dump(prefixes, f)
                        with open('required files/prefixes.json', 'r') as f:
                            getPrefix = json.load(f)
                        guildPrefix = getPrefix[str(ctx.guild.id)]['prefix'].split()
                        with open("required files/prefixes.json") as f:
                            prefixes = json.load(f)

                        async def prefix(self, ctx):
                            id = ctx.guild.id
                            guildPrefix=prefixes[str(ctx.guild.id)]["prefix"].split()
                            return prefixes[str(ctx.guild.id)]["prefix"].split()
                        self.bot.command_prefix=prefix
                        await ctx.send(f"Prefix has been changed to `{value.split()}`")
            else:
                if not value:
                    return await ctx.send(f"This guild's prefixes are `{prefixes[str(ctx.guild.id)]['prefix'].split()}`")
                else:
                    if (not (str(ctx.guild.id) in prefixes)):
                        prefixes[str(ctx.guild.id)] = {

                        }
                        prefixes[str(ctx.guild.id)]['prefix'] = "t! T! t. T."
                        with open('required files/prefixes.json', 'w') as f:
                            json.dump(prefixes, f)
                    with open('required files/prefixes.json', 'r') as f:
                        prefixes[str(ctx.guild.id)]['prefix'] = str(value)
                    with open('required files/prefixes.json', 'w') as f:
                        json.dump(prefixes, f)
                    with open('required files/prefixes.json', 'r') as f:
                        getPrefix = json.load(f)
                    guildPrefix = getPrefix[str(ctx.guild.id)]['prefix'].split()
                    with open("required files/prefixes.json") as f:
                        prefixes = json.load(f)

                    async def prefix(self, ctx):
                        id = ctx.guild.id
                        guildPrefix=prefixes[str(ctx.guild.id)]["prefix"].split()
                        return prefixes[str(ctx.guild.id)]["prefix"].split()
                    self.bot.command_prefix=prefix
                    await ctx.send(f"Prefix has been changed to `{value.split()}`")
        elif setting.lower()=="welcome":
            with open('required files/channels.json', 'r') as f:
                channels = json.load(f)
            if not await ctx.bot.is_owner(ctx.author):
                if not ctx.author.guild_permissions.administrator:
                    try:
                        welcomeChannel=discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['welcome']))
                        return await ctx.send(f"This guild's welcome channel is {welcomeChannel.mention}")
                    except Exception as E:
                        raise E
                        return await ctx.send("There was a problem getting this guild's welcome channel. It probably hasn't been set yet.")
                else:
                    if not value:
                        try:
                            welcomeChannel=discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['welcome']))
                            return await ctx.send(f"This guild's welcome channel is {welcomeChannel.mention}")
                        except Exception as E:
                            raise E
                            return await ctx.send("There was a problem getting this guild's welcome channel. It probably hasn't been set yet.")
                    else:
                        try:
                            newWelcomeChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                            WelcomeChannelID=str(newWelcomeChannel.id)
                            channels[str(ctx.guild.id)]['welcome']=WelcomeChannelID
                            with open("required files/channels.json", "w") as f:
                                json.dump(channels, f)
                            return await ctx.send(f"This guild's welcome channel has been set to {newWelcomeChannel.mention}")
                        except:
                            return await ctx.send("Couldn't find that channel. Make sure you typed the name exactly.")
            else:
                if not value:
                    try:
                        welcomeChannel=discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['welcome']))
                        return await ctx.send(f"This guild's welcome channel is {welcomeChannel.mention}")
                    except Exception as E:
                        raise E
                        return await ctx.send("There was a problem getting this guild's welcome channel. It probably hasn't been set yet.")
                else:
                    try:
                        newWelcomeChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                        WelcomeChannelID=str(newWelcomeChannel.id)
                        channels[str(ctx.guild.id)]['welcome']=WelcomeChannelID
                        with open("required files/channels.json", "w") as f:
                            json.dump(channels, f)
                        return await ctx.send(f"This guild's welcome channel has been set to {newWelcomeChannel.mention}")
                    except:
                        return await ctx.send("Couldn't find that channel. Make sure you typed the name exactly.")
        elif setting.lower()=="rules":
            with open('required files/channels.json', 'r') as f:
                channels = json.load(f)
            if not await ctx.bot.is_owner(ctx.author):
                if not ctx.author.guild_permissions.administrator:
                    try:
                        rulesChannel=discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['rules']))
                        return await ctx.send(f"This guild's rules channel is {rulesChannel.mention}")
                    except:
                        return await ctx.send("There was a problem getting this guild's rules channel. It probably hasn't been set yet.")
                else:
                    if not value:
                        try:
                            rulesChannel=await discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['rules']))
                            return await ctx.send(f"This guild's rules channel is {rulesChannel.mention}")
                        except:
                            return await ctx.send("There was a problem getting this guild's rules channel. It probably hasn't been set yet.")
                    else:
                        try:
                            newRulesChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                            RulesChannelID=str(newRulesChannel.id)
                            channels[str(ctx.guild.id)]['rules']=RulesChannelID
                            with open("required files/channels.json", "w") as f:
                                json.dump(channels, f)
                            return await ctx.send(f"This guild's rules channel has been set to {newRulesChannel.mention}")
                        except:
                            return await ctx.send("Couldn't find that channel. Make sure you typed the name exactly.")
            else:
                if not value:
                    try:
                        rulesChannel=await discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['rules']))
                        return await ctx.send(f"This guild's rules channel is {rulesChannel.mention}")
                    except:
                        return await ctx.send("There was a problem getting this guild's rules channel. It probably hasn't been set yet.")
                else:
                    try:
                        newRulesChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                        RulesChannelID=str(newRulesChannel.id)
                        channels[str(ctx.guild.id)]['rules']=RulesChannelID
                        with open("required files/channels.json", "w") as f:
                            json.dump(channels, f)
                        return await ctx.send(f"This guild's rules channel has been set to {newRulesChannel.mention}")
                    except:
                        return await ctx.send("Couldn't find that channel. Make sure you typed the name exactly.")
        elif setting.lower()=="levelup":
            with open('required files/channels.json', 'r') as f:
                channels = json.load(f)
            if not ctx.author.guild_permissions.administrator:
                try:
                    lvlUpChannel=discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['levelup']))
                    return await ctx.send(f"This guild's rules channel is {lvlUpChannel.mention}")
                except:
                    return await ctx.send("There was a problem getting this guild's level up channel.  It probably hasn't been set yet.")
            else:
                if not value:
                    try:
                        lvlUpChannel=discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['levelup']))
                        return await ctx.send(f"This guild's level up channel is {rulesChannel.mention}")
                    except:
                        return await ctx.send("There was a problem getting this guild's level up channel. It probably hasn't been set yet.")
                else:
                    try:
                        newLvlUpChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                        lvlUpChannelID=str(newLvlUpChannel.id)
                        channels[str(ctx.guild.id)]['levelup']=lvlUpChannelID
                        with open("required files/channels.json", "w") as f:
                            json.dump(channels, f)
                        return await ctx.send(f"This guild's level up channel has been set to {newLvlUpChannel.mention}")
                    except:
                        return await ctx.send("Couldn't find that channel. Make sure you typed the name exactly.")
        elif setting.lower()=="noxp":
            if not ctx.author.guild_permissions.administrator:
                with open("required files/banned_channels.txt", "a+") as f:
                    bannedList=f.read().strip().split()
                embed=discord.Embed(title="Messages in these channels will not gain XP", color=65280)
                embed.description=""
                for channel in ctx.guild.text_channels:
                    if str(channel.id) in bannedList:
                        embed.description+=f"{channel.mention}\n"
                if embed.description=="":
                    return await ctx.send("All channels will gain XP")
                await ctx.send(embed=embed)
            if not value:
                with open("required files/banned_channels.txt", "r") as f:
                    bannedList=f.read().strip().split()
                embed=discord.Embed(title="Messages in these channels will not gain XP", color=65280)
                embed.description=""
                for channel in ctx.guild.text_channels:
                    if str(channel.id) in bannedList:
                        embed.description+=f"{channel.mention}\n"
                if embed.description=="":
                    return await ctx.send("All channels will gain XP")
                await ctx.send(embed=embed)
            else:
                with open("required files/banned_channels.txt", "r") as f:
                    bannedList=f.read().strip().split()
                try:
                    newBannedXPChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                    bannedXPChannelID=str(newBannedXPChannel.id)
                    if str(bannedXPChannelID) in bannedList:
                        return await ctx.send(f"{newBannedXPChannel.mention} is already banned from gaining XP")
                    else:
                        with open("required files/banned_channels.txt", "a+") as f:
                            f.write(f"{str(bannedXPChannelID)}\n")
                        return await ctx.send(f"Messages in {newBannedXPChannel.mention} will no longer gain XP")
                except:
                    await ctx.send("Couldn't find that channel. Make sure you typed the name exactly.")
        elif setting.lower()=="gainxp":
            if not ctx.author.guild_permissions.administrator:
                return await ctx.send("You don't have permission to set which channels gain XP")
            elif not value:
                return await ctx.send("You didn't specify which channel to allow XP gain in.")
            else:
                try:
                    allowedChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                    allowedChannelID=str(allowedChannel.id)
                    with open("required files/banned_channels.txt", "r") as f:
                        bannedList=f.read()
                    if str(allowedChannelID) in bannedList:
                        with open("required files/banned_channels.txt", "r") as f:
                            lines = f.readlines()
                        with open("required files/banned_channels.txt", "w") as f:
                            for line in lines:
                                if line.strip("\n") != allowedChannelID:
                                    f.write(line)
                        return await ctx.send(f"Messages in {allowedChannel.mention} will now gain XP")
                    else:
                        return await ctx.send(f"{allowedChannel.mention} is already able to gain XP")
                    with open("required files/banned_channels.txt", "r") as f:
                        lines = f.readlines()
                    with open("required files/banned_channels.txt", "w") as f:
                        for line in lines:
                            if line.strip("\n") != allowedChannelID:
                                f.write(line)
                    return await ctx.send(f"Messages in {allowedChannel.mention} will now gain XP")
                except:
                    return await ctx.send("Couldn't find that channel. Make sure you typed the name exactly")
        elif setting.lower()=="addrole":
            if not ctx.author.guild_permissions.administrator:
                return await ctx.send("You don't have permission to add roles")
            elif not value:
                return await ctx.send("You didn't specify which role to add")
            else:
                try:
                    allowedRole=discord.utils.get(ctx.guild.roles, name=value)
                    allowedRoleID=allowedRole.id
                    with open('required files/roles.json', 'r') as f:
                        roles = json.load(f)
                    if not str(ctx.guild.id) in roles:
                        roles[str(ctx.guild.id)] = {

                        }
                        roles[str(ctx.guild.id)]['roles'] = []
                        with open('required files/roles.json', 'w') as f:
                            json.dump(roles, f)
                    with open("required files/roles.json", "r") as f:
                        roles=json.load(f)
                    if allowedRoleID in roles[str(ctx.guild.id)]["roles"]:
                        return await ctx.send(f"{allowedRole.name} is already an assignable role")
                    else:
                        roles[str(ctx.guild.id)]["roles"].append(allowedRoleID)
                        with open("required files/roles.json", "w") as f:
                            json.dump(roles, f)
                        return await ctx.send(f"{allowedRole.name} had been added. You can now join it using **join {allowedRole.name}**")
                except:
                    await ctx.send("Couldn't find that role. Make sure you typed the name exactly")
        elif setting.lower()=="removerole":
            if not ctx.author.guild_permissions.administrator:
                return await ctx.send("You don't have permission to remove roles")
            elif not value:
                return await ctx.send("You didn't specify which role to remove")
            else:
                try:
                    allowedRole=discord.utils.get(ctx.guild.roles, name=value)
                    allowedRoleID=allowedRole.id
                    with open('required files/roles.json', 'r') as f:
                        roles = json.load(f)
                    if not str(ctx.guild.id) in roles:
                        return await ctx.send(f"{allowedRole.name} isn't an assignable role.")
                    roles[str(ctx.guild.id)]["roles"].remove(allowedRoleID)
                    with open("required files/roles.json", "w") as f:
                        json.dump(roles, f)
                    return await ctx.send(f"{allowedRole.name} is no longer an assignable role.")
                except:
                    await ctx.send("Couldn't find that role. Make sure you typed the name exactly")
        elif setting.lower()=="logging":
            with open('required files/channels.json', 'r') as f:
                channels = json.load(f)
            if not await ctx.bot.is_owner(ctx.author):
                if not ctx.author.guild_permissions.administrator:
                    try:
                        logChannel=discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['log']))
                        return await ctx.send(f"This guild's logging channel is {logChannel.mention}")
                    except:
                        return await ctx.send("There was a problem getting this guild's logging channel. It probably hasn't been set yet.")
                else:
                    if not value:
                        try:
                            logChannel=await discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['log']))
                            return await ctx.send(f"This guild's logging channel is {logChannel.mention}")
                        except:
                            return await ctx.send("There was a problem getting this guild's logging channel. It probably hasn't been set yet.")
                    else:
                        try:
                            newLogChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                            LogChannelID=str(newLogChannel.id)
                            channels[str(ctx.guild.id)]['log']=LogChannelID
                            with open("required files/channels.json", "w") as f:
                                json.dump(channels, f)
                            return await ctx.send(f"This guild's logging channel has been set to {newLogChannel.mention}")
                        except:
                            return await ctx.send("Couldn't find that channel. Make sure you typed the name exactly.")
            else:
                if not value:
                    try:
                        logChannel=await discord.utils.get(ctx.guild.text_channels, id=int(channels[str(ctx.guild.id)]['log']))
                        return await ctx.send(f"This guild's logging channel is {logChannel.mention}")
                    except:
                        return await ctx.send("There was a problem getting this guild's logging channel. It probably hasn't been set yet.")
                else:
                    try:
                        newLogChannel = discord.utils.get(ctx.guild.text_channels, name=value)
                        logChannelID=str(newLogChannel.id)
                        channels[str(ctx.guild.id)]['log']=logChannelID
                        with open("required files/channels.json", "w") as f:
                            json.dump(channels, f)
                        return await ctx.send(f"This guild's logging channel has been set to {newLogChannel.mention}")
                    except:
                        return await ctx.send("Couldn't find that channel. Make sure you typed the name exactly.")

        else:
            embed=discord.Embed(title="Settings", description="If you just want to view the setting, you don't need to specify a value.\n<> denotes a required argument. [] denotes an optional argument.\nFor example:  **t!settings welcome** will show you the welcome channel.", color=65280)
            embed.add_field(name="Changing settings", value="""**welcome [channel name]** - Sets or shows you the welcome channel.
**rules [channel name]** - Sets or shows you the rules channel.
**levelup [channel name]** - Sets or shows you the level up channel.
**noxp [channel name]** - Sets or shows you the channels in which messages will not gain XP.
**gainxp <channel name>** - Allows a channel to gain XP again.
**addrole <role name>** - Allows a role to be self-assignable.
**removerole <role name>** - Stops a role from being self-assignable.
**prefix [values separated by a space]** - Sets or shows you this guild's prefixes.

Channel names do not require the # but do require the -'s if there are any.
Role names must be exact when adding them, but do not need to be exact when joining or leaving them.""", inline=False)
            embed.set_footer(text="Takagibot - written by apex#2504")
            return await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Configuration(bot))
