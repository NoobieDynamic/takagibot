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
import datetime

startup_extensions = ['cogs.moderation', 'cogs.economy', 'cogs.roles', 'cogs.utility', 'cogs.levels', 'cogs.fun', 'cogs.config', 'cogs.dbl']
with open("required files/prefixes.json") as f:
    prefixes = json.load(f)



def prefix(bot, message):
    guild=message.guild
    with open('required files/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    if (not (str(guild.id) in prefixes)):
        prefixes[str(guild.id)] = {

        }
        prefixes[str(guild.id)]['prefix'] = "t! T! t. T."
        with open('required files/prefixes.json', 'w') as f:
            json.dump(prefixes, f)
    with open('required files/prefixes.json', 'r') as f:
        getPrefix = json.load(f)
    guildPrefix = getPrefix[str(guild.id)]['prefix'].split()
    bot.command_prefix=prefix
    with open('required files/channels.json', 'r') as f:
        channels = json.load(f)
    if (not (str(guild.id) in channels)):
        channels[str(guild.id)] = {

        }
        channels[str(guild.id)]['welcome'] = ""
        channels[str(guild.id)]['rules'] = ""
        channels[str(guild.id)]['levelup'] = ""
        with open('required files/channels.json', 'w') as f:
            json.dump(channels, f)
    with open('required files/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    id = message.guild.id
    guildPrefix=prefixes[str(message.guild.id)]["prefix"]
    return prefixes[str(message.guild.id)]["prefix"].split()

bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
bot.remove_command('help')
bot.bootTime=datetime.datetime.utcnow()
with open("config.json", "r") as ff:
    conf=json.load(ff)
token=conf["token"]
bot.gapi=conf["google"]
bot.discordbotsapi=conf["dbl"]

@bot.event
async def on_ready():
    try:
        bot.load_extension('cogs.music4')
        print("Loaded music4")
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to  load extension {extension}\n{exc}')
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Game(name='with Nishikata - t!help'))


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to  load extension {extension}\n{exc}')

@bot.event
async def on_member_join(member):
    try:
        with open('required files/channels.json', 'r') as f:
            channels = json.load(f)
        guildWelcomeChannel = channels[str(member.guild.id)]['welcome']
        guildRulesChannel = channels[str(member.guild.id)]['rules']
        channel = bot.get_channel(int(guildWelcomeChannel))
        rule_channel = bot.get_channel(int(guildRulesChannel))
        await channel.send(f"Welcome to {member.guild.name}, **{member.name}**! Please read the rules ({rule_channel.mention}) as soon as possible".format(member, rule_channel))
    except:
        pass

@bot.event
async def on_guild_join(guild):
    with open('required files/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    if (not (str(guild.id) in prefixes)):
        prefixes[str(guild.id)] = {

        }
        prefixes[str(guild.id)]['prefix'] = "t! T! t. T."
        with open('required files/prefixes.json', 'w') as f:
            json.dump(prefixes, f)
    with open('required files/prefixes.json', 'r') as f:
        getPrefix = json.load(f)
    guildPrefix = getPrefix[str(guild.id)]['prefix'].split()
    bot.command_prefix=prefix
    with open('required files/channels.json', 'r') as f:
        channels = json.load(f)
    if (not (str(guild.id) in channels)):
        channels[str(guild.id)] = {

        }
        channels[str(guild.id)]['welcome'] = ""
        channels[str(guild.id)]['rules'] = ""
        channels[str(guild.id)]['levelup'] = ""
        with open('required files/channels.json', 'w') as f:
            json.dump(channels, f)
    newDict={}
    with open("required files/"+str(guild.id)+".json", "w") as out:
        json.dump(newDict, out)



#--------------------------------------------------------------------------------------------------------------------------------


@bot.command(name="load")
async def load(ctx, cog=None):
    if await ctx.bot.is_owner(ctx.author):
        if not cog:
            await ctx.send("You didn't say which cog to load")
        else:
            try:
                bot.load_extension("cogs."+str(cog))
                await ctx.send("`{}` has been loaded".format(cog))
            except Exception as E:
                await ctx.send(f"There was a problem loading `{cog}`, ```{E}```")
    else:
        await ctx.send("Only the bot owner can manage extensions.")

@bot.command(name="unload")
async def unload(ctx, cog=None):
    if await ctx.bot.is_owner(ctx.author):
        if not cog:
            await ctx.send("You didn't say which cog to load")
        else:
            try:
                bot.unload_extension("cogs."+str(cog))
                await ctx.send("`{}` has been unloaded".format(cog))
            except Exception as E:
                await ctx.send(f"There was a problem unloading `{cog}`, ```{E}```")
    else:
        await ctx.send("You don't have permission to manage extensions.")

@bot.command(name="reload")
async def reload(ctx, cog=None):
    if await ctx.bot.is_owner(ctx.author):
        if not cog:
            await ctx.send("You didn't say which cog to load")
        else:
            try:
                bot.unload_extension("cogs."+str(cog))
                bot.load_extension("cogs."+str(cog))
                await ctx.send("`{}` has been reloaded".format(cog))
            except Exception as E:
                await ctx.send(f"There was a problem reloading `{cog}`, ```{E}```")
    else:
        await ctx.send("You don't have permission to manage extensions.")

#--------------------------------------------------------------------------------------------------------------------------------

bot.run(token)
