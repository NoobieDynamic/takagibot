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
import sqlite3
from discord.ext import commands
import asyncio
import datetime
import time

now = str(datetime.datetime.utcnow())[8:(- 16)]
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name='daily')
    async def daily(self, ctx):
        global now
        current = str(datetime.datetime.utcnow())[8:(- 16)]
        if current != now:
            economy2 = sqlite3.connect('required files/Economy.db')
            c2 = economy2.cursor()
            newDoneDaily = '0'
            c2.executemany('UPDATE Users SET HasDoneDaily=?', (newDoneDaily,))
            economy2.commit()
            now = current
        economy = sqlite3.connect('required files/Economy.db')
        c = economy.cursor()
        c.execute('SELECT UserID FROM Users WHERE UserID=?', (str(ctx.author.id),))
        idNum = str(c.fetchall())
        hasBoughtEG=None
        hasBoughtGAP=None
        alreadyDoneDaily=None
        startingBalance="10"
        alreadyDoneDaily=None
        if idNum == "[]":
            economy3 = sqlite3.connect('required files/Economy.db')
            c3 = economy3.cursor()
            hasBoughtEG = '0'
            hasBoughtGAP = '0'
            alreadyDoneDaily = '1'
            c3.execute('INSERT INTO Users (UserID, Money, HasDoneDaily, EpicGamer, GiveawayAccess) VALUES (?, ?, ?, ?, ?);', (str(ctx.author.id), startingBalance, alreadyDoneDaily, hasBoughtEG, hasBoughtGAP))
            embed = discord.Embed(description='Welcome {0.mention}, you have received your 10 daily credits'.format(ctx.author), color=65280)
            await ctx.send(embed=embed)
            economy3.commit()
            return
        c.execute('SELECT UserID FROM Users WHERE UserID=?', (str(ctx.author.id),))
        idNum = str(c.fetchall())
        Number = idNum[2:(- 3)]
        c.execute('SELECT HasDoneDaily FROM Users WHERE UserID=?', (str(ctx.author.id),))
        alreadyDoneDaily = str(c.fetchall())[2:(- 3)]
        if alreadyDoneDaily == '0':
            if str(ctx.author.id) in idNum:
                alreadyDoneDaily = 1
                embed = discord.Embed(description='{0.mention}, you have received your 10 daily credits'.format(ctx.author), color=65280)
                await ctx.send(embed=embed)
                MoneyUser = ctx.author
                balance = c.execute('SELECT Money FROM Users WHERE UserID = (?)', (Number,))
                balance2 = str(c.fetchall())[2:(- 3)]
                balance3 = int(float(balance2))
                newBalance = balance3 + 10
                c.execute('UPDATE Users SET Money = ? WHERE UserID = ?', (newBalance, Number))
                c.execute('UPDATE Users SET HasDoneDaily = ? WHERE UserID = ?', (alreadyDoneDaily, Number))
                economy.commit()
        else:
            dt = datetime.datetime.now()
            tomorrow = dt + datetime.timedelta(days=1)
            diff = datetime.datetime.combine(tomorrow, datetime.time.min) - dt
            diff = str(diff)[:(- 7)]
            diffH = diff[:(- 6)]
            diffM = diff[len(diffH) + 1:(- 3)]
            diffS = diff[(len(diffH) + len(diffM)) + 2:]
            embed = discord.Embed(description='{0.mention}, you have already received your daily credits! Credits reset in **{1} hours, {2} minutes and {3} seconds**'.format(ctx.author, diffH, diffM, diffS), color=65280)
            await ctx.send(embed=embed)

    @commands.command(name='balance', aliases=['bal', 'credits'] )
    async def balance(self, ctx):
        checker = ctx.author
        economy = sqlite3.connect('required files/Economy.db')
        c = economy.cursor()
        rawBalance = c.execute('SELECT Money FROM Users WHERE UserID == ?', (str(ctx.author.id),))
        PrintBalance = c.fetchall()
        Balance = str(PrintBalance)[2:(- 3)]
        if PrintBalance:
            embed = discord.Embed(description='{0.mention}, you have **{1}** credits'.format(checker, Balance), color=65280)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="{0.mention}, you don't have any credits. Use `t!daily` to get started.'".format(checker), color=65280)
            await ctx.send(embed=embed)

    @commands.command(name="gift", aliases=["give"])
    async def gift(self, ctx, recipient:discord.Member=None, giftAmount:int=None):
        startingBalance=None
        alreadyDoneDaily=None
        hasBoughtEG=None
        hasBoughtGAP=None
        if not giftAmount:
            await ctx.send("There was a problem.")
            return
        elif ctx.author.id==recipient.id:
            await ctx.send("You can't give yourself credits!")
            return
        elif giftAmount<0:
            await ctx.send("You can't give people negative credits!")
            return
        elif giftAmount==0:
            await ctx.send("You can't give people zero credits!")
            return
        else:
            startGifting=sqlite3.connect("required files/Economy.db")
            c=startGifting.cursor()
            c.execute('SELECT Money FROM Users WHERE UserID=?', (str(ctx.author.id),))
            currentCash=str(c.fetchall())[2:-3]
            currentCashInt=int(currentCash)
            if giftAmount<=currentCashInt:
                recipientID=str(recipient.id)
                c.execute('SELECT Money FROM Users WHERE UserID=?', (recipientID,))
                DBrecipientID=str(c.fetchall())
                if DBrecipientID=="[]":
                    startingBalance="0"
                    alreadyDoneDaily="0"
                    hasBoughtEG="0"
                    hasBoughtGAP="0"
                    c.execute('INSERT INTO Users (UserID, Money, HasDoneDaily, EpicGamer, GiveawayAccess) VALUES (?, ?, ?, ?, ?);', (recipientID, startingBalance, alreadyDoneDaily, hasBoughtEG, hasBoughtGAP))
                    startGifting.commit()
                c.execute('SELECT Money FROM Users WHERE UserID=?', (recipientID,))
                recipientCurrentCash=int(str(c.fetchall())[2:-3])
                newRecipientCash=recipientCurrentCash+giftAmount
                newRecipientCashString=str(newRecipientCash)
                newSenderCash = currentCashInt-giftAmount
                newSenderCashString=str(newSenderCash)
                c.execute('UPDATE Users SET Money = ? WHERE UserID = ?', (newSenderCashString, str(ctx.author.id)))
                startGifting.commit()
                c.execute('UPDATE Users SET Money = ? WHERE UserID = ?', (newRecipientCashString, str(recipientID)))
                startGifting.commit()
                await ctx.send(":white_check_mark: **{}**, you have given **{}** `{}` credits".format(ctx.author.name, recipient.name, str(giftAmount)))
            else:
                await ctx.send(":x: **{}**, you don't have enough credits to do that! Use t!credits to check your balance.".format(ctx.author.name))
                return

    @gift.error
    async def gift_error(self, ctx, error):
        embed=discord.Embed(title="Usage", description = "`t!gift <recipient name/mention> <amount>`", color=65280)
        await ctx.send(embed=embed)


    @commands.command(name='shop')
    async def shop(self, ctx, action=None, item: int = None):
        await ctx.send("The shop is currently closed. Check back later")
        return
        if not action:
            embed = discord.Embed(title=':shopping_cart: Shop', color=65280)
            embed.add_field(name='Items', value='**1**⠀⠀Epic gamers role\n⠀⠀⠀Price: 200 credits\n\n**2**⠀⠀Giveaway access pass\n⠀⠀⠀Price: 50 credits', inline=False)
            embed.set_footer(text='Use `t!shop buy <number>` to buy an item')
            await ctx.send(embed=embed)
            return
        elif action.lower() == "buy":
            if not item:
                embed=discord.Embed(title="Usage", description = """`t!shop` shows you all the available items\n`t!shop buy <number>` buys an item\nIf you don't have any credits, use `t!daily` to get started""", color=65280)
                await ctx.send(embed=embed)
            elif item == 1:
                try:
                    buying = sqlite3.connect('required files/Economy.db')
                    c = buying.cursor()
                    c.execute('SELECT EpicGamer FROM Users WHERE UserID=?', (str(ctx.author.id),))
                    isEpicGamer = str(c.fetchall())
                    Number = isEpicGamer[2:(- 3)]
                    if Number == '0':
                        c.execute('SELECT Money FROM Users WHERE UserID=?', (str(ctx.author.id),))
                        currentMoney = str(c.fetchall())
                        shortMoney = currentMoney[2:(- 3)]
                        shortMoneyInt = int(shortMoney)
                        newMoney = shortMoneyInt - 200
                        if newMoney < 0:
                            await ctx.send((':x: ' + ctx.author.mention) + ", you don't have enough credits to buy that!")
                            return
                        else:
                            newEpicGamer = ctx.author
                            egRole = discord.utils.get(newEpicGamer.guild.roles, name='Epic Gamers')
                            await newEpicGamer.add_roles(egRole)
                            newValue = '1'
                            c.execute('UPDATE Users SET EpicGamer = ? WHERE UserID = ?', (newValue, str(ctx.author.id)))
                            c.execute('UPDATE Users SET Money = ? WHERE UserID = ?', (newMoney, str(ctx.author.id)))
                            buying.commit()
                            await ctx.send((':white_check_mark: ' + ctx.author.mention) + ', you have bought **Epic gamers role**!')
                    else:
                        await ctx.send(':x: '+ctx.author.mention + ', you already have that item!')
                        return
                except:
                        await ctx.send(ctx.author.mention + ", you don't have any credits. Use `t!daily` to get started.")
                        return

            elif item == 2:
                try:
                    buying = sqlite3.connect('required files/Economy.db')
                    c = buying.cursor()
                    c.execute('SELECT GiveawayAccess FROM Users WHERE UserID=?', (str(ctx.author.id),))
                    hasAccess = str(c.fetchall())
                    Number = hasAccess[2:(- 3)]
                    if Number == '0':
                            c.execute('SELECT Money FROM Users WHERE UserID=?', (str(ctx.author.id),))
                            currentMoney = str(c.fetchall())
                            shortMoney = currentMoney[2:(- 3)]
                            shortMoneyInt = int(shortMoney)
                            newMoney = shortMoneyInt - 50
                            if newMoney < 0:
                                await ctx.send((':x: ' + ctx.author.mention) + ", you don't have enough credits to buy that!")
                                return
                            else:
                                newAccess = ctx.author
                                gaRole = discord.utils.get(newAccess.guild.roles, name='Giveaway Access Pass')
                                await newAccess.add_roles(gaRole)
                                newValue = '1'
                                c.execute('UPDATE Users SET GiveawayAccess = ? WHERE UserID = ?', (newValue, str(ctx.author.id)))
                                c.execute('UPDATE Users SET Money = ? WHERE UserID = ?', (newMoney, str(ctx.author.id)))
                                buying.commit()
                                await ctx.send((':white_check_mark: ' + ctx.author.mention) + ', you have bought **Giveaway access pass**!')

                    else:
                        await ctx.send((':x: ' + ctx.author.mention) + ', you already have that item!')
                        return
                except:
                    await ctx.send(ctx.author.mention + ", you don't have any credits. Use `t!daily` to get started.")
                    return
            else:
                await ctx.send((':x: ' + ctx.author.mention) + ", that isn't a valid item. Use `t!shop` too see whats available.")
                return
        else:
            embed=discord.Embed(title="Usage", description = """`t!shop` shows you all the available items\n`t!shop buy <number>` buys an item\nIf you don't have any credits, use `t!daily` to get started""", color=65280)
            await ctx.send(embed=embed)

    @shop.error
    async def shop_error(self, ctx, error):
        embed=discord.Embed(title="Usage", description = """`t!shop` shows you all the available items\n`t!shop buy <number>` buys an item\nIf you don't have any credits, use `t!daily` to get started""", color = 65280)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
