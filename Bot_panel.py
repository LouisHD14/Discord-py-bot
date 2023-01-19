import asyncio
import json
import os
from os.path import isfile, join
import discord
from discord.ext import commands
from pathlib import Path
import requests


intents = discord.Intents.all()
bot = commands.Bot(intents=intents, 
                command_prefix='!',
                sync_commands=True,
	            delete_not_existing_commands=True,
                )

# change playing status
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="am chillen"))
    await bot.tree.sync()

if os.path.isfile("servers.json"):
    with open('servers.json', encoding='utf-8') as f:
        servers = json.load(f)
else:
    servers = {"servers": []}
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)
        
@bot.hybrid_command(description="Sends a random waifu image")
async def waifu(ctx):
    if ctx.channel.id == 1063569015760506880:
        response = requests.get('https://waifu.pics/api/nsfw/waifu')
        data = response.json()
        if 'url' in data:
            url = data['url']
            embed = discord.Embed(
                title="Waifu",
                description=f"Here is your waifu {ctx.author.mention}!",
                )
            embed.set_footer(text="Powered by waifu.pics")
            embed.set_image(url=url)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("Sorry, there was an error getting the image.")
    else:
        await ctx.channel.send(f"{ctx.author.mention}, Du bist nen Huen und kannst das nicht benutzen.")


"""
@bot.event
async def on_message(message):
    if message.author.id == 787966688808534026:
        await message.channel.send("huen")
    elif message.author.id == 761581955338338304:
        await message.channel.send("Geh Fortnite spielen")
    elif message.author.id == 714097888791232651:
        await message.channel.send("huen")
"""

@bot.hybrid_command()
async def activate(ctx):
    if ctx.author.guild_permissions.administrator:
        if not guild_exists(ctx.guild.id):
            server = {
                "guildid": ctx.guild.id,
                "guildname": ctx.guild.name,
                "invite": f'{(await ctx.channel.create_invite()).url}',
                "guildownername": ctx.guild.owner.name,
                "guildownerid": ctx.guild.owner.id,
            }
            servers["servers"].append(server)
            with open('servers.json', 'w') as f:
                json.dump(servers, f, indent=4)
            await ctx.send(f'Bot für **{ctx.guild.name}** aktiviert')
            print(f'Bot für **{ctx.guild.name}** aktiviert')
            print(f"Daten von {ctx.guild.name} wurden gespeichert")

@bot.hybrid_command(description="Löscht X Nachrichten.")
async def clear(ctx, num: int, target: discord.Member=None):
    if num > 500 or num < 0:
        return await ctx.send("Ungültige Angabe. Maximum ist 500.")
    def msgcheck(amsg):
        if target:
           return amsg.author.id == target.id
        return True
    deleted = await ctx.channel.purge(limit=num, check=msgcheck)
    await ctx.send(f'**{len(deleted)}/{num}** Nachrichten wurden gelöscht.', delete_after=10)

@bot.hybrid_command()
async def deactivate(ctx):
     if ctx.author.guild_permissions.administrator:
        if guild_exists(ctx.guild.id):
            globalid = get_guild_id(ctx.guild.id)
            if globalid != -1:
                servers["servers"].pop(globalid)
                with open('servers.json', 'w') as f:
                    json.dump(servers, f, indent=4)
            await ctx.send(f'Bot für **{ctx.guild.name}** deaktiviert')
            print(f'Bot für **{ctx.guild.name}** deaktiviert')
            print(f"Daten von {ctx.guild.name} gelöscht")



###############################

def guild_exists(guildid):
    for server in servers['servers']:
        if int(server['guildid'] == int(guildid)):
            return True
    return False



def get_guild_id(guild_id):
    guild_id_ = -1
    i = 0
    for server in servers["servers"]:
        if int(server["guildid"]) == int(guild_id):
            guild_id_ = i
        i += 1
    return guild_id_


###########################################################

async def load_extensions():
    for filename in os.listdir(r"C:\Users\Louis_HD\Desktop\python\Discord_Bot\cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded extension {filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        #await bot.load_extension(f"cogs.activate")
        await bot.start("MTAzODQ2MDQxODk0OTEyNDIxOA.G9X1JE.Z4qHYSegwE_R_TpauDuDPQESR4RUXe4mL46Wwo")
        

#asyncio.run(main())

bot.run("")

