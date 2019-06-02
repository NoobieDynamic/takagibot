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
import aiohttp
import random
from PIL import Image, ImageDraw, ImageFont
import os


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name='thank', aliases = ["ty"])
    async def thank(self, ctx, *, userName: discord.Member=None):
        if (not userName):
            await ctx.send(file=discord.File("required files/Thank You Kanye.jpg"))
        else:
            img=Image.open("required files/very cool.png")
            font=ImageFont.truetype("required files/Helvetica.ttf", 35)
            d=ImageDraw.Draw(img)
            text=f"Thank you {userName.name}, very cool!"
            d.text((40, 135), text, font=font, fill=(50,50,50))
            img.save("Very Cool Image.png")
            await ctx.send(file=discord.File("Very Cool Image.png"))
            os.remove("Very Cool Image.png")


    @thank.error
    async def thank_error(self, ctx, error):
        await ctx.send('You need to enter a valid user to thank!')

    @commands.command(name='oopsie')
    async def oopsie(self, ctx, *, userName: discord.Member=None):
        if (not userName):
            embed = discord.Embed(description='Who did an oopsie?', color=65280)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(description=userName.mention + ' did an oopsie!', color=65280)
            await ctx.send(embed=embed)

    @oopsie.error
    async def oopsie_error(self, ctx, error):
        await ctx.send('{}, you did an oopsie by mentioning an invalid user!'.format(ctx.author.mention))
    msg = None

    @commands.command(name='poll')
    async def poll(self, ctx, contents=None, emoteOne=None, emoteTwo=None):
        global msg
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("You don't have permission to start polls.")
            return
        question = str(ctx.message.content)[7:]
        embed = discord.Embed(color=65280)
        creator = str(ctx.author)
        embed.add_field(name='New poll by ' + creator, value=contents, inline=False)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(emoteOne)
        await msg.add_reaction(emoteTwo)
        await ctx.message.delete()

    @poll.error
    async def poll_error(self, ctx, error):
        global msg
        embed = discord.Embed(title='Usage', description='`t!poll "question" optionOne optionTwo`\nYou cannot use custom emojis for reactions.', color=65280)
        await ctx.send(embed=embed)
        await msg.delete()

    @commands.command(name='giveaway')
    async def giveaway(self, ctx, EndDate: int, *, prize:str):
        if not ctx.author.guild_permissions.administrator:
                await ctx.send("You do not have permission to start giveaways")
                return
        embed = discord.Embed(title='Giveaway!\nReact with :tada: to enter!', description=prize, color=65280)
        embed.set_footer(text='Ends in {} days'.format(EndDate))
        startGiveaway = await ctx.send(embed=embed)
        with open("required files/giveaways.json", "r") as f:
            giveaways=json.load(f)
        if not str(ctx.guild.id) in giveaways:
            giveaways[str(ctx.guild.id)]={}
            with open("required files/giveaways.json", "w") as f:
                json.dump(giveaways, f)
        with open("required files/giveaways.json", "r") as f:
            giveaways=json.load(f)
        giveaways[str(ctx.guild.id)]["prize"]=prize
        giveaways[str(ctx.guild.id)]["end"]=str(EndDate)
        giveaways[str(ctx.guild.id)]["message_id"]=str(startGiveaway.id)
        with open("required files/giveaways.json", "w") as f:
            giveaways=json.dump(giveaways, f)
        await startGiveaway.add_reaction(u"\U0001F389")
        await ctx.message.delete()
        #EndDate*60*60*24
        await asyncio.sleep(EndDate*60*60*24)
        with open("required files/giveaways.json", "r") as f:
            giveawayRetrieve=json.load(f)
        giveawayMsgID = int(giveawayRetrieve[str(ctx.guild.id)]["message_id"])
        entries=None
        winner=None
        newGiveawayMsg = await ctx.channel.fetch_message(giveawayMsgID)
        react=newGiveawayMsg.reactions
        for item in react:
             entries=await item.users().flatten()
        winner=random.choice(entries)
        while winner == self.bot.user:
            winner=random.choice(entries)
        await ctx.send(f'''**Giveaway ended**
Congrats, {winner.mention}, you won **{giveawayRetrieve[str(ctx.guild.id)]["prize"]}**!''')

    @giveaway.error
    async def giveaway_error(self, ctx, error):
        embed=discord.Embed(color=65280)
        embed.add_field(name="Usage", value="""**giveaway <number of days> <prize>**
Giveaways will be drawn automatically after the specified number of days""")
        await ctx.send(embed=embed)

    @commands.command(name='subcount', aliases =["sc"])
    async def subcount(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=pewdiepie&key="+self.bot.gapi) as resp:
                dataP=await resp.text()
            async with session.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=tseries&key="+self.bot.gapi) as resp:
                dataT=await resp.text()
        subsP = json.loads(dataP)['items'][0]['statistics']['subscriberCount']
        subsT = json.loads(dataT)['items'][0]['statistics']['subscriberCount']
        diff = int(subsP) - int(subsT)
        ahead=None
        if diff>0:
            ahead="PewDiePie is leading by {:,d} subscribers".format(diff)
        elif diff<0:
            diff=diff*-1
            ahead="T-Series is leading by {:,d} subscribers".format(diff)
        else:
            ahead="PewDiePie and T-series are equal!"
        embed = discord.Embed(color=65280)
        embed.add_field(name='PewDiePie subscribers', value='{:,d}'.format(int(subsP)), inline=True)
        embed.add_field(name='T-Series subscribers', value='{:,d}'.format(int(subsT)), inline=True)
        embed.add_field(name='Subscriber difference', value=ahead, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="dog")
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as resp:
                data=await resp.text()
        info=json.loads(data)["message"]
        embed=discord.Embed(color=65280)
        embed.add_field(name="Here is your random dog", value=f"[Link to download image]({info})")
        embed.set_image(url=info)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
