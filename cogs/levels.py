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
from PIL import Image as image
from PIL import ImageDraw as imagedraw
from PIL import ImageFont as imagefont
import PIL
import numpy as np
from PIL import Image, ImageDraw
from os.path import basename
from os.path import join
import os
import aiohttp

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    async def update_data(self, users, user):
        if (not (str(user.id) in users)):
            users[str(user.id)] = {

            }
            users[str(user.id)]['experience'] = 0
            users[str(user.id)]['level'] = 1


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
                    await channel.send('{} has reached level {}!'.format(user.mention, lvl_end))
                except:
                    pass
                users[str(user.id)]['level'] = lvl_end
        except:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("required files/"+str(member.guild.id)+".json", 'r') as f:
            users = json.load(f)
        await self.update_data(users, member)
        with open("required files/"+str(member.guild.id)+".json", 'w') as f:
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
                with open("required files/"+str(message.guild.id)+".json", 'r') as f:
                    users = json.load(f)
            except:
                newDict={}
                with open("required files/"+str(message.guild.id)+".json", "w") as out:
                    json.dump(newDict, out)
            with open("required files/"+str(message.guild.id)+".json", 'r') as f:
                users = json.load(f)
            await self.update_data(users, message.author)
            await self.add_xp(users, message.author, 10, message)
            await self.level_up(users, message.author, message.channel, message)
            with open("required files/"+str(message.guild.id)+".json", 'w') as f:
                json.dump(users, f)


    @commands.command(name='rank', aliases=["level"])
    async def rank(self, ctx, userExp=None):
        if (not userExp):
            with open("required files/"+str(ctx.guild.id)+".json", 'r') as f:
                users = json.load(f)
            try:
                xpCount = users[str(ctx.author.id)]['experience']
                lvl = users[str(ctx.author.id)]['level']
            except:
                return await ctx.send("That user doesnt have a rank")
            position = sorted(users, key=(lambda x: users[x]['experience']), reverse=True)
            number = 1
            embed = None
            for ID in position:
                numberstr = str(number)
                number = number + 1
                authorShort=None
                if str(ctx.author.id) == ID:
                    async with aiohttp.ClientSession() as session:
                            async with session.get(str(ctx.author.avatar_url)) as resp:
                                data=await resp.read()
                    with open(str(ctx.author.id)+".gif", mode="wb") as f:
                        f.write(data)

                    img = image.new("RGB", (1200, 400), color = (37, 40, 45))

                    font=imagefont.truetype("required files/Product Sans Bold.ttf", 80)
                    d=imagedraw.Draw(img)
                    if len(str(ctx.author)) > 12:
                        authorShort=str(ctx.author)[:12] + '...'
                    else:
                        authorShort=str(ctx.author)
                    text=str(authorShort)
                    d.text((430, 60), text, font=font, fill=(255, 255, 255))
                    font=imagefont.truetype("required files/Product Sans Bold.ttf", 50)
                    d=imagedraw.Draw(img)
                    text="Leaderboard rank {}".format(number-1)
                    d.text((430, 150), text, font=font, fill=(255, 255, 255))
                    text="Level {}".format(lvl)
                    d.text((430, 200), text, font=font, fill=(255, 255, 255))
                    text="{} XP".format(xpCount)
                    d.text((430, 250), text, font=font, fill=(255, 255, 255))

                    img.save("PILdraw.png")


                    import numpy as np
                    from PIL import Image, ImageDraw

                    # Open the input image as numpy array, convert to RGB
                    img=Image.open(str(ctx.author.id)+".gif").convert("RGB")
                    npImage=np.array(img)
                    h,w=img.size

                    # Create same size alpha layer with circle
                    alpha = Image.new('L', img.size,0)
                    draw = ImageDraw.Draw(alpha)
                    draw.pieslice([0,0,h,w],0,360,fill=255)

                    # Convert alpha Image to numpy array
                    npAlpha=np.array(alpha)

                    # Add alpha layer to RGB
                    npImage=np.dstack((npImage,npAlpha))

                    # Save with alpha
                    Image.fromarray(npImage).save('result.png')

                    img = Image.open('result.png')
                    img = img.resize((300,300), PIL.Image.ANTIALIAS)
                    img.save('result.png')


                    background = Image.open("PILdraw.png")
                    foreground = Image.open("result.png")

                    background.paste(foreground, (100, 50), foreground)
                    background.save("card.png")
                    await ctx.send(file=discord.File("card.png"))
                    os.remove("PILdraw.png")
                    os.remove("result.png")
                    os.remove("card.png")
                    os.remove(str(ctx.author.id)+".gif")
        else:
            if len(userExp)<3:
                await ctx.send("That name is too short. Try mentioning them instead.")
                return
            try:
                foundUserRank=ctx.message.mentions[0]
                userExpPing = str(foundUserRank.id)
                for person in ctx.guild.members:
                    if str(foundUserRank.name).lower() in str(person).lower():
                        with open("required files/"+str(ctx.guild.id)+".json", 'r') as f:
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
                            foundUserRankShort=None
                            if userExpPing == ID:
                                async with aiohttp.ClientSession() as session:
                                        async with session.get(str(foundUserRank.avatar_url)) as resp:
                                            data=await resp.read()
                                with open(str(foundUserRank.id)+".gif", mode="wb") as f:
                                    f.write(data)

                                img = image.new("RGB", (1200, 400), color = (37, 40, 45))

                                font=imagefont.truetype("required files/Product Sans Bold.ttf", 80)
                                d=imagedraw.Draw(img)
                                if len(str(foundUserRank)) > 12:
                                    foundUserRankShort=str(foundUserRank)[:12] + '...'
                                else:
                                    foundUserRankShort=str(foundUserRank)
                                text=str(foundUserRankShort)
                                d.text((430, 60), text, font=font, fill=(255, 255, 255))
                                font=imagefont.truetype("required files/Product Sans Bold.ttf", 50)
                                d=imagedraw.Draw(img)
                                text="Leaderboard rank {}".format(number-1)
                                d.text((430, 150), text, font=font, fill=(255, 255, 255))
                                text="Level {}".format(lvl)
                                d.text((430, 200), text, font=font, fill=(255, 255, 255))
                                text="{} XP".format(xpCount)
                                d.text((430, 250), text, font=font, fill=(255, 255, 255))

                                img.save("PILdraw.png")


                                import numpy as np
                                from PIL import Image, ImageDraw

                                # Open the input image as numpy array, convert to RGB
                                img=Image.open(str(foundUserRank.id)+".gif").convert("RGB")
                                npImage=np.array(img)
                                h,w=img.size

                                # Create same size alpha layer with circle
                                alpha = Image.new('L', img.size,0)
                                draw = ImageDraw.Draw(alpha)
                                draw.pieslice([0,0,h,w],0,360,fill=255)

                                # Convert alpha Image to numpy array
                                npAlpha=np.array(alpha)

                                # Add alpha layer to RGB
                                npImage=np.dstack((npImage,npAlpha))

                                # Save with alpha
                                Image.fromarray(npImage).save('result.png')

                                img = Image.open('result.png')
                                img = img.resize((300,300), PIL.Image.ANTIALIAS)
                                img.save('result.png')


                                background = Image.open("PILdraw.png")
                                foreground = Image.open("result.png")

                                background.paste(foreground, (100, 50), foreground)
                                background.save("card.png")
                                await ctx.send(file=discord.File("card.png"))
                                os.remove("PILdraw.png")
                                os.remove("result.png")
                                os.remove("card.png")
                                os.remove(str(foundUserRank.id)+".gif")
            except:
                for person in ctx.guild.members:
                    if userExp.lower() in str(person).lower():
                        rankID=str(person.id)
                        with open("required files/"+str(ctx.guild.id)+".json", 'r') as f:
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
                            personShort=None
                            if str(MentionID) == ID:
                                userMention = person.name
                                async with aiohttp.ClientSession() as session:
                                        async with session.get(str(person.avatar_url)) as resp:
                                            data=await resp.read()
                                with open(str(person.id)+".gif", mode="wb") as f:
                                    f.write(data)

                                img = image.new("RGB", (1200, 400), color = (37, 40, 45))

                                font=imagefont.truetype("required files/Product Sans Bold.ttf", 80)
                                d=imagedraw.Draw(img)
                                if len(str(person)) > 12:
                                    personShort=str(person)[:12] + '...'
                                else:
                                    personShort=str(person)
                                text=str(personShort)
                                d.text((430, 60), text, font=font, fill=(255, 255, 255))
                                font=imagefont.truetype("required files/Product Sans Bold.ttf", 50)
                                d=imagedraw.Draw(img)
                                text="Leaderboard rank {}".format(number-1)
                                d.text((430, 150), text, font=font, fill=(255, 255, 255))
                                text="Level {}".format(lvl)
                                d.text((430, 200), text, font=font, fill=(255, 255, 255))
                                text="{} XP".format(xpCount)
                                d.text((430, 250), text, font=font, fill=(255, 255, 255))

                                img.save("PILdraw.png")


                                import numpy as np
                                from PIL import Image, ImageDraw

                                # Open the input image as numpy array, convert to RGB
                                img=Image.open(str(person.id)+".gif").convert("RGB")
                                npImage=np.array(img)
                                h,w=img.size

                                # Create same size alpha layer with circle
                                alpha = Image.new('L', img.size,0)
                                draw = ImageDraw.Draw(alpha)
                                draw.pieslice([0,0,h,w],0,360,fill=255)

                                # Convert alpha Image to numpy array
                                npAlpha=np.array(alpha)

                                # Add alpha layer to RGB
                                npImage=np.dstack((npImage,npAlpha))

                                # Save with alpha
                                Image.fromarray(npImage).save('result.png')

                                img = Image.open('result.png')
                                img = img.resize((300,300), PIL.Image.ANTIALIAS)
                                img.save('result.png')


                                background = Image.open("PILdraw.png")
                                foreground = Image.open("result.png")

                                background.paste(foreground, (100, 50), foreground)
                                background.save("card.png")
                                await ctx.send(file=discord.File("card.png"))
                                os.remove("PILdraw.png")
                                os.remove("result.png")
                                os.remove("card.png")
                                os.remove(str(person.id)+".gif")
                                return
                await ctx.send("There was a problem getting the rank for that user.")


    @rank.error
    async def rank_error(self, ctx, error):
        await ctx.send("There was a problem getting the rank for that user")

    @commands.command(name='top', aliases=["leaderboard"])
    async def top(self, ctx):
        WillDelete = await ctx.send('<a:loading:567065920992706589> Getting data...')
        with open("required files/"+str(ctx.guild.id)+".json", 'r') as f:
            users = json.load(f)
        high_score_list_xp = sorted(users, key=(lambda x: users[x]['experience']), reverse=True)
        high_score_list = sorted(users, key=(lambda x: users[x]['experience']), reverse=True)
        place = ''
        name = ''
        totalXP = ''
        number = 1
        message = ''
        for Name in high_score_list:
            if number < 11:
                usersXP = users[Name]
                nameID = await self.bot.fetch_user(Name)
                IDname = nameID.name
                if number == 10:
                    message += ((('[' + str(number)) + ']     ') + IDname)
                else:
                    message += ((('[' + str(number)) + ']      ') + IDname)
                usersXP = users[Name]['experience']
                usersLevel=users[Name]['level']
                message+="\n         Level "+str(usersLevel)
                message += "\n⠀⠀⠀⠀⠀⠀ ⠀Total score: "+str(usersXP) + ' XP\n'
                xpCounts = str(users[str(ctx.author.id)]['experience'])
            if str(ctx.author.id) == Name:
                messageAdd = (((('---------------------------------------\n' + ctx.author.name) + ', you currently have ') + str(xpCounts)) + ' XP and are in position ') + str(number)
            number += 1
        message += messageAdd
        await ctx.send(('```' + message) + '```')
        await WillDelete.delete()

def setup(bot):
    bot.add_cog(Levels(bot))
