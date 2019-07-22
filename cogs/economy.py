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

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name='daily')
    async def daily(self, ctx):
        current = datetime.datetime.utcnow().day
        if current != self.bot.now:
            economy2 = sqlite3.connect('required files/Economy.db')
            c2 = economy2.cursor()
            newDoneDaily = '0'
            c2.executemany('UPDATE Users SET HasDoneDaily=?', (newDoneDaily,))
            economy2.commit()
            self.bot.now = current
        economy = sqlite3.connect('required files/Economy.db')
        c = economy.cursor()
        c.execute('SELECT UserID FROM Users WHERE UserID=?', (str(ctx.author.id),))
        idNum = str(c.fetchall())
        alreadyDoneDaily=None
        startingBalance="10"
        alreadyDoneDaily=None
        if idNum == "[]":
            economy3 = sqlite3.connect('required files/Economy.db')
            c3 = economy3.cursor()
            alreadyDoneDaily = '1'
            c3.execute('INSERT INTO Users (UserID, Money, HasDoneDaily) VALUES (?, ?, ?);', (str(ctx.author.id), startingBalance, alreadyDoneDaily))
            await ctx.send('Welcome {0.mention}, you have received your first 10 credits'.format(ctx.author))
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
                await ctx.send('{0.mention}, you have received your 10 daily credits'.format(ctx.author))
                MoneyUser = ctx.author
                balance = c.execute('SELECT Money FROM Users WHERE UserID = (?)', (Number,))
                balance2 = str(c.fetchall())[2:(- 3)]
                balance3 = int(float(balance2))
                newBalance = balance3 + 10
                c.execute('UPDATE Users SET Money = ? WHERE UserID = ?', (newBalance, Number))
                c.execute('UPDATE Users SET HasDoneDaily = ? WHERE UserID = ?', (alreadyDoneDaily, Number))
                economy.commit()
        else:
            dt = datetime.datetime.utcnow()
            tomorrow = dt + datetime.timedelta(days=1)
            diff = datetime.datetime.combine(tomorrow, datetime.time.min) - dt
            diff = str(diff)[:(- 7)]
            diffH = diff[:(- 6)]
            diffM = diff[len(diffH) + 1:(- 3)]
            diffS = diff[(len(diffH) + len(diffM)) + 2:]
            await ctx.send('{0.mention}, you have already received your daily credits! Credits reset in **{1} hours, {2} minutes and {3} seconds**'.format(ctx.author, diffH, diffM, diffS))

    @commands.command(name='balance', aliases=['bal', 'credits'] )
    async def balance(self, ctx):
        checker = ctx.author
        economy = sqlite3.connect('required files/Economy.db')
        c = economy.cursor()
        rawBalance = c.execute('SELECT Money FROM Users WHERE UserID == ?', (str(ctx.author.id),))
        PrintBalance = c.fetchall()
        Balance = str(PrintBalance)[2:(- 3)]
        if PrintBalance:
            await ctx.send('{0.mention}, you have **{1}** credits'.format(checker, Balance))
        else:
            await ctx.send("{0.mention}, you don't have any credits. Use `t!daily` to get started.".format(checker))


    @commands.command(name="gift", aliases=["give"])
    async def gift(self, ctx, recipient:discord.Member=None, giftAmount:int=None):
        startingBalance=None
        alreadyDoneDaily=None
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
                    c.execute('INSERT INTO Users (UserID, Money, HasDoneDaily) VALUES (?, ?, ?);', (recipientID, startingBalance, alreadyDoneDaily))
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



def setup(bot):
    bot.add_cog(Economy(bot))
