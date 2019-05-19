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

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick')
    async def kick(self, ctx, *, userName: discord.Member=None):
        if ctx.author.guild_permissions.kick_members:
            if (not userName):
                await ctx.send('You need to specify who to kick.')
                await ctx.send(embed=embed)
                return
            else:
                try:
                    await userName.kick()
                    await ctx.send('User has been kicked from the server.')
                except:
                    await ctx.send(f"I can't kick {userName.name} because they are an admin or mod.")
        else:
            await ctx.send("You don't have permission to do that.")

    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.send("Please enter a valid member. Either mention them or use their name (not nickname)")
        return

    @commands.command(name='ban')
    async def ban(self, ctx, *, userName: discord.Member=None):
        if ctx.author.guild_permissions.ban_members:
            if (not userName):
                await ctx.send('You need to specify who to ban.')
                await ctx.send(embed=embed)
                return
            else:
                try:
                    await userName.ban()
                    await ctx.send('User has been banned from the server.')
                except:
                    await ctx.send(f"I can't ban {userName.name} because they are an admin or mod.")
        else:
            await ctx.send("You don't have permission to do that.")

    @ban.error
    async def ban_error(self, ctx, error):
        await ctx.send("Please enter a valid member. Either mention them or use their name (not nickname)")
        return

    @commands.command(name='mute')
    async def mute(self, ctx, userName: discord.Member=None, time=None):
        if ctx.author.guild_permissions.kick_members:
            if (not userName):
                await ctx.send('You need to specify who to mute.')
                return
            else:
                try:
                    for role in ctx.guild.roles:
                        if role.name=="Muted":
                            await userName.add_roles(role, reason=f"Muted by {ctx.author}")
                            if not time:
                                await ctx.send(f"**{userName}** has been muted")
                                return
                            else:
                                try:
                                    if time[-1:]=="m":
                                        timeScale=time[:-1]
                                        await ctx.send(f"**{userName}** has been muted for {timeScale} minutes")
                                        await asyncio.sleep(int(timeScale)*60)
                                        await userName.remove_roles(role, reason=f"{ctx.author}: Time's up")
                                        await ctx.send(f"Time's up! **{userName}** has been unmuted.")
                                        return
                                    elif time[-1:]=="h":
                                        timeScale=time[:-1]
                                        await ctx.send(f"**{userName}** has been muted for {timeScale} hours")
                                        await asyncio.sleep(int(timeScale)*60*60)
                                        await userName.remove_roles(role, reason=f"{ctx.author}: Time's up")
                                        await ctx.send(f"Time's up! **{userName}** has been unmuted.")
                                        return
                                    elif time[-1:]=="d":
                                        timeScale=time[:-1]
                                        await ctx.send(f"**{userName}** has been muted for {timeScale} days")
                                        await asyncio.sleep(int(timeScale)*60*60*24)
                                        await userName.remove_roles(role, reason=f"{ctx.author}: Time's up")
                                        await ctx.send(f"Time's up! **{userName}** has been unmuted.")
                                        return
                                    else:
                                        await ctx.send("You can enter `m` (minutes), `h` (hours), or `d` (days)")
                                        return
                                except:
                                    await ctx.send("""You entered an invalid time.
`mute @member` mutes a member until you decide to unmute them
`mute @member 10m` mutes them for 10 minutes
`mute @member 1h` mutes them for 1 hour
`mute @member 7d` mutes them for 7 days.""")
                                    return
                    deleteAfterMute=await ctx.send("<a:loading:567065920992706589> This guild doesn't have a Muted role. I'm adding one now.")
                    await ctx.guild.create_role(name="Muted")
                    MuteNow=discord.utils.get(ctx.guild.roles, name="Muted")
                    await userName.add_roles(MuteNow)
                    for channel in ctx.guild.channels:
                        if isinstance(channel, discord.TextChannel):
                            await channel.set_permissions(MuteNow, send_messages=False)
                        elif isinstance(channel, discord.VoiceChannel):
                            await channel.set_permissions(MuteNow, speak=False)
                    await deleteAfterMute.delete()
                    await ctx.send(f"**{userName}** has been muted.")
                except Exception as e:
                    await deleteAfterMute.delete()
                    await ctx.send(f"There was a problem: ```{e}```")
        else:
            await ctx.send("You don't have permission to do that")

    @mute.error
    async def mute_error(self, ctx, error):
        await ctx.send("Please enter a valid member. Either mention them or use their name (not nickname)")
        return


    @commands.command(name='unmute')
    async def unmute(self, ctx, *, userName: discord.Member=None):
        if ctx.author.guild_permissions.kick_members:
            if (not userName):
                await ctx.send('You need to specify who to unmute.')
                return
            else:
                try:
                    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
                    await userName.remove_roles(mutedRole, reason=f"Unmuted by {ctx.author}")
                    await ctx.send(f"**{userName.name}** has been unmuted.")
                except:
                    await ctx.send("I don't have permission to unmute people.")
        else:
            await ctx.send("You don't have permission to do that")

    @unmute.error
    async def unmute_error(self, ctx, error):
        await ctx.send("Please enter a valid member. Either mention them or use their name (not nickname)")
        return

    @commands.command(name='clear', aliases=["purge"])
    async def clear(self, ctx, amount=None):
        if ctx.author.guild_permissions.manage_messages:
            if (not amount):
                embed = discord.Embed(description='You need to specify the number of messages to delete.', color=65280)
                await ctx.send(embed=embed)
                return
            else:
                amount = int(amount) + 1
                deleteNumber = await ctx.channel.purge(limit=amount)
                amount=amount-1
                embed = discord.Embed(description='Cleared {0} messages.'.format(amount), color=65280)
                await ctx.send(embed=embed, delete_after=10)
        else:
            return await ctx.send("You don't have permission to manage messages")



def setup(bot):
    bot.add_cog(Moderation(bot))
