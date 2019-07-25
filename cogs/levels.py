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
import json
import asyncio
import os
import aiohttp
import PIL
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    async def update_data(self, users, user):
        if (not (str(user.id) in users)):
            users[str(user.id)] = {

            }
            users[str(user.id)]['experience'] = 0
            users[str(user.id)]['level'] = 0


    async def add_xp(self, users, user, xp, message):
        users[str(user.id)]['experience'] += xp

    async def level_up(self, users, user, channel, message):
        with open("required files/channels.json", "r") as f:
            lvlUpChannel=json.load(f)
        try:
            experience = users[str(user.id)]['experience']
            lvl_start = users[str(user.id)]['level']
            lvl_end = int(experience ** (1 / 4))
            if lvl_start < lvl_end:
                try:
                    messageHere=int(lvlUpChannel[str(message.guild.id)]["levelup"])
                    channel = self.bot.get_channel(messageHere)
                    await channel.send(f'**{user.name}** has reached level {lvl_end}!')
                except:
                    pass
                users[str(user.id)]['level'] = lvl_end
        except:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("guild levels/"+str(member.guild.id)+".json", 'r') as f:
            users = json.load(f)
        await self.update_data(users, member)
        with open("guild levels/"+str(member.guild.id)+".json", 'w') as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        with open("required files/banned_channels.txt", "r") as f:
            bannedList=f.read()
        if not message.guild:
            pass
        elif str(message.channel.id) in bannedList:
            pass
        else:
            try:
                with open("guild levels/"+str(message.guild.id)+".json", 'r') as f:
                    users = json.load(f)
            except:
                newDict={}
                with open("guild levels/"+str(message.guild.id)+".json", "w") as out:
                    json.dump(newDict, out)
            with open("guild levels/"+str(message.guild.id)+".json", 'r') as f:
                users = json.load(f)
            await self.update_data(users, message.author)
            await self.add_xp(users, message.author, 10, message)
            await self.level_up(users, message.author, message.channel, message)
            with open("guild levels/"+str(message.guild.id)+".json", 'w') as f:
                json.dump(users, f)

    async def generate_rank_card(self, ctx, user, number, lvl, xpCount):
        async with aiohttp.ClientSession() as session:
                async with session.get(str(user.avatar_url)) as resp:
                    data=await resp.read()
        with open(str(user.id)+".png", mode="wb") as f:
            f.write(data)

        fg=Image.open(str(user.id)+".png").convert("RGBA")
        fg = fg.resize((300,300), PIL.Image.ANTIALIAS)
        bg = Image.open("required files/avatarBG.png")
        bg.paste(fg, (0, 0), fg)
        bg.save(str(user.id)+".png")

        mask = Image.new("L", fg.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0,0, fg.size[0], fg.size[1]), fill=255)

        result = bg.copy()
        result.putalpha(mask)

        result.save("result.png")

        img = Image.open('result.png')

        img = Image.open("required files/base.png")

        font=ImageFont.truetype("required files/Product Sans Bold.ttf", 80)
        d=ImageDraw.Draw(img)
        shortName=None
        if len(str(user.name)) > 14:
            shortName=str(user.name)[:14] + '...'
        else:
            shortName=str(user.name)
        text=str(shortName)
        d.text((430, 60), text, font=font, fill=(255, 255, 255))
        font=ImageFont.truetype("required files/Product Sans Bold.ttf", 50)
        d=ImageDraw.Draw(img)
        text="Leaderboard rank {}".format(number-1)
        d.text((430, 150), text, font=font, fill=(255, 255, 255))
        text="Level {}".format(lvl)
        d.text((430, 200), text, font=font, fill=(255, 255, 255))
        text="{} XP".format(xpCount)
        d.text((430, 250), text, font=font, fill=(255, 255, 255))

        img.save("PILdraw.png")


        background = Image.open("PILdraw.png").convert('RGBA')
        foreground = Image.open("result.png").convert('RGBA')

        background.paste(foreground, (100, 50), foreground)
        background.save("card.png")
        await ctx.send(file=discord.File("card.png"))

        os.remove("PILdraw.png")
        os.remove("result.png")
        os.remove("card.png")
        os.remove(str(user.id)+".png")
        return

    @commands.command(name='rank', aliases=["level"])
    async def rank(self, ctx, *, userExp=None):
        async with ctx.channel.typing():
            pass
        if (not userExp):
            with open("guild levels/"+str(ctx.guild.id)+".json", 'r') as f:
                users = json.load(f)
            try:
                xpCount = users[str(ctx.author.id)]['experience']
                lvl = users[str(ctx.author.id)]['level']
            except:
                return await ctx.send("You don't have a rank")
            position = sorted(users, key=(lambda x: users[x]['experience']), reverse=True)
            number = 1
            embed = None
            for ID in position:
                numberstr = str(number)
                number = number + 1
                if str(ctx.author.id) == ID:
                    await self.generate_rank_card(ctx, ctx.author, number, lvl, xpCount)
                    return
        else:
            if len(userExp)<3:
                await ctx.send("That name is too short. Try mentioning them instead.")
                return
            try:
                foundUserRank=ctx.message.mentions[0]
                userExpPing = str(foundUserRank.id)
                for person in ctx.guild.members:
                    if str(foundUserRank.name).lower() in str(person).lower():
                        with open("guild levels/"+str(ctx.guild.id)+".json", 'r') as f:
                            users = json.load(f)
                        try:
                            xpCount = users[str(userExpPing)]['experience']
                            lvl = users[str(userExpPing)]['level']
                        except:
                            return await ctx.send("That user doesn't have a rank")
                        position = sorted(users, key=(lambda x: users[x]['experience']), reverse=True)
                        number = 1
                        embed = None
                        for ID in position:
                            numberstr = str(number)
                            number = number + 1
                            if userExpPing == ID:
                                await self.generate_rank_card(ctx, foundUserRank, number, lvl, xpCount)
                                return
            except:
                for person in ctx.guild.members:
                    if userExp.lower() in str(person).lower():
                        rankID=str(person.id)
                        with open("guild levels/"+str(ctx.guild.id)+".json", 'r') as f:
                            users = json.load(f)
                        try:
                            xpCount = users[str(rankID)]['experience']
                            lvl = users[rankID]['level']
                        except:
                            return await ctx.send("That user doesn't have a rank")
                        position = sorted(users, key=(lambda x: users[x]['experience']), reverse=True)
                        number = 1
                        embed = None
                        for ID in position:
                            MentionID = rankID
                            numberstr = str(number)
                            number = number + 1
                            if str(MentionID) == ID:
                                await self.generate_rank_card(ctx, person, number, lvl, xpCount)
                                return
        await ctx.send("Couldn't find that user. Try mentioning them in the command.")



    @rank.error
    async def rank_error(self, ctx, error):
        await ctx.send("There was a problem getting the rank for that user")

    @commands.command(name='top', aliases=["leaderboard"])
    async def top(self, ctx, page:int=None):
        with open("guild levels/"+str(ctx.guild.id)+".json", 'r') as f:
            users = json.load(f)
        if not page:
            page=1
        start=((page-1)*10)+1
        end=page*10
        high_score_list = sorted(users, key=(lambda x: users[x]['experience']), reverse=True)
        place = ''
        name = ''
        totalXP = ''
        number = 1
        message = ''
        for Name in high_score_list:
            if number<start:
                number+=1
                continue
            if number <= end:
                usersXP = users[Name]
                nameID = self.bot.get_user(int(Name))
                if nameID is None:
                    number-=1
                else:
                    IDname = nameID.name
                    if len(str(number)) >1:
                        message += ((('[' + str(number)) + ']     ') + IDname)
                    else:
                        message += ((('[' + str(number)) + ']      ') + IDname)
                    usersXP = users[Name]['experience']
                    usersLevel=users[Name]['level']
                    message+="\n         Level "+str(usersLevel)
                    message += "\n⠀⠀⠀⠀⠀⠀ ⠀Total score: "+str(usersXP) + ' XP\n'
            else:
                break
            number+=1
        number=1
        for Name in high_score_list:
            if str(ctx.author.id) == Name:
                xpCounts = str(users[str(ctx.author.id)]['experience'])
                messageAdd = (((('---------------------------------------\n' + ctx.author.name) + ', you currently have ') + str(xpCounts)) + ' XP and are in position ') + str(number)
                break
            else:
                number += 1
        message += messageAdd
        message='```' + message + '```'
        await ctx.send(message)



def setup(bot):
    bot.add_cog(Levels(bot))
