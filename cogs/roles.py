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

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name='join', aliases=["role", "joinrole",])
    async def join(self, ctx, *, role=None):
        if (not role):
            await ctx.send("You haven't specified which role you want to join.")
            return
        with open("required files/roles.json", "r") as f:
            roles=json.load(f)
        for guildRole in ctx.guild.roles:
            if role.lower() in str(guildRole.name).lower():
                if guildRole.id in roles[str(ctx.guild.id)]["roles"]:
                    roleUser=ctx.author
                    joinedRole=discord.utils.get(ctx.guild.roles, name=str(guildRole.name))
                    await roleUser.add_roles(joinedRole)
                    await ctx.send("You have joined **{}**".format(str(guildRole.name)))
                    return
        else:
            await ctx.send("That's not a valid role.")

    @join.error
    async def join_error(self, ctx, error):
        await ctx.send("There was a problem. Either this guild doesn't have any assignable roles, the requested role is higher than my highest role, or I don't have permission.")

    @commands.command(name='leave', aliases=["leaverole"])
    async def leave(self, ctx, *, role:str=None):
        if (not role):
            await ctx.send("You haven't specified which role you want to leave.")
            return
        with open("required files/roles.json", "r") as f:
            roles=json.load(f)
        for guildRole in ctx.guild.roles:
            if role.lower() in str(guildRole.name).lower():
                if guildRole.id in roles[str(ctx.guild.id)]["roles"]:
                    roleUser=ctx.author
                    joinedRole=discord.utils.get(ctx.guild.roles, name=str(guildRole.name))
                    await roleUser.remove_roles(joinedRole)
                    await ctx.send("You have left **{}**".format(str(guildRole.name)))
                    return
        else:
            await ctx.send("That's not a valid role.")

    @leave.error
    async def leave_error(self, ctx, error):
        await ctx.send("There was a problem. Either this guild doesn't have any assignable roles, the requested role is higher than my highest role, or I don't have permission.")


    @commands.command(name="roles", aliases=["ranks"])
    async def roles(self, ctx):
        with open("required files/roles.json", "r") as f:
            roles=json.load(f)
        rolesMessage=""
        try:
            for roleID in roles[str(ctx.guild.id)]["roles"]:
                roleInfo=discord.utils.get(ctx.guild.roles, id=roleID)
                roleName=roleInfo.name
                rolesMessage+=roleName+"\n"
            embed=discord.Embed(color=65280)
            embed.add_field(name="Assignable roles", value=rolesMessage)
            return await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("This guild doesn't have any assignable roles")
            raise e




def setup(bot):
    bot.add_cog(Roles(bot))
