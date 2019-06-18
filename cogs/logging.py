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
import asyncio
import json
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open("required files/channels.json", "r") as f:
            data=json.load(f)
        try:
            logChannel=await self.bot.fetch_channel(int(data[str(message.guild.id)]['log']))
            embed=discord.Embed(title=f"Message deleted in {message.channel}", color=65280)
            embed.add_field(name=f"{message.author}", value=message.content)
            await logChannel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        with open("required files/channels.json", "r") as f:
            data=json.load(f)
        try:
            logChannel=await self.bot.fetch_channel(int(data[str(after.guild.id)]['log']))
            embed=discord.Embed(title=f"Message edited by {after.author} in {after.channel}", color=65280)
            before_content=None
            after_content=None
            if before.content is None:
                before_content="*Embed or image*"
            else:
                before_content=before.content
            if after.content is None:
                after_content="*Embed or image"
            else:
                after_content=after.content
            embed.add_field(name="Original message", value=before_content, inline=False)
            embed.add_field(name="New message", value=after_content, inline=False)
            await logChannel.send(embed=embed)
        except:
            pass



def setup(bot):
    bot.add_cog(Logging(bot))
