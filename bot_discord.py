import asyncio
import json
import random
import discord
from discord import guild
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import pytz
from datetime import datetime


############################################################################################################################################################################





bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")

############################################################################################################################################################################

@bot.event
async def on_ready():
    print(f"Eingeloggt als '{bot.user.name}'")
    await bot.change_presence(activity=discord.Game("Hunter's Fivem Stuff"))


############################################################################################################################################################################

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    if user == None:
        await ctx.send("Please enter a user!")
        return

    await user.kick(reason=reason)
    await ctx.send(f'Kicked {user.name} for reason {reason}')


############################################################################################################################################################################

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member = None, *, reason=None):
    if user == None:
        await ctx.send("Bitte gebe einen User ein!")
        return
  
    await user.ban(reason=reason)
    await ctx.send(f'***{user.name} • {user.id}*** gebannt für den Grund: ***{reason}***')

############################################################################################################################################################################

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User, *, reason = None): # Step 1
  if reason is None: # Step 2 - part 1
    reason = "Kein Grund." # Step 2 - part 2
  guild = ctx.guild # Step 3
  try: # Step 4 - part 1
    await guild.unban(user, reason=reason) # Step 5
  except: # Step 4 - part 2
    return await ctx.send("User existiert nicht oder wurde nicht gebannt.") # Step 4 - part 3
  await ctx.send(f"User: ***{user}*** erfolgreich entbannt.") # Step 6

############################################################################################################################################################################

@bot.command(name='announce')
async def announce(ctx, *args):
    de = pytz.timezone("Europe/Berlin")
    colour = 0xe74c3c
    embed = discord.Embed(title="Announce für Hunter's Fivem Stuff", description="", color=colour, timestamp=datetime.now().astimezone(tz=de))

    embed.add_field(name=f'Angefordert von: {ctx.author.name}', value=f'```{" ".join(args)}```', inline="True")

    await ctx.send(f"<@&1031221917044191404>")
    await ctx.send(embed=embed)

############################################################################################################################################################################




@bot.command()
async def Commands(ctx):
    de = pytz.timezone("Europe/Berlin")
    colour = 0x979c9f
    embed = discord.Embed(title=f"**Commands**", description="", color=colour, timestamp=datetime.now().astimezone(tz=de))


    embed.add_field(name="!Commands", value=f"```Zeigt diese Hilfe an```", inline="True")
    embed.add_field(name="!ban", value=f"```Bannt einen User vom Discord```", inline="True")
    embed.add_field(name="!unban", value=f"```Entbannt einen User```", inline="True")
    embed.add_field(name="!kick", value=f"```Kickt einen User vom Discord```", inline="True")
    embed.add_field(name="!userinfo", value=f"```Zeigt dir Infos eines Users```", inline="True")
    embed.add_field(name="!anounce", value=f"```Schickt eine Anounce```", inline="True")

    await ctx.send(embed=embed)

############################################################################################################################################################################


@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member):
    de = pytz.timezone("Europe/Berlin")
    colour = random.randint(0, 0xFFFFFF)
    embed = discord.Embed(title=f"Userinfo für: {member.name}", description="", color=colour, timestamp=datetime.now().astimezone(tz=de))


    embed.add_field(name="Name", value=f"```{member.name}#{member.discriminator}```", inline="True")
    embed.add_field(name="Bot", value=f"```{('Ja' if member.bot else 'Nein')}```", inline="True")
    embed.add_field(name="Nickname", value=f"```{(member.nick if member.nick else 'nicht gesetzt')}```", inline="True")
    embed.add_field(name="Server beigetreten", value=f"```{member.joined_at}```", inline="True")
    embed.add_field(name="Discord beigtreten", value=f"```{member.created_at}```", inline="True")
    embed.add_field(name="Rollen", value=f"```{len(member.roles)}```", inline="True")
    embed.add_field(name="Höchste Rolle", value=f"```{member.top_role.name}```", inline="True")
    embed.add_field(name="Farbe", value=f"```{member.color}```", inline="True")
    embed.add_field(name="Booster", value=f"```{('Ja' if member.premium_since else 'Nein')}```", inline="True")

    embed.set_footer(text=f'Angefordert von {ctx.author.name} • {ctx.author.id}', icon_url=ctx.author.avatar.url)

    await ctx.send(embed=embed)

############################################################################################################################################################################


@bot.command(description="Löscht X Nachrichten.")
async def clear(ctx, num: int, target: discord.Member=None):
    if num > 500 or num < 0:
        return await ctx.send("Ungültige Angabe. Maximum ist 500.")
    def msgcheck(amsg):
        if target:
           return amsg.author.id == target.id
        return True
    deleted = await ctx.channel.purge(limit=num, check=msgcheck)
    await ctx.send(f'**{len(deleted)}/{num}** Nachrichten wurden gelöscht.', delete_after=10)

############################################################################################################################################################################

@bot.command()
async def write(ctx, *, text):
    with open("./bans.json", "r") as f:
        data = json.load(f)
    data[ctx.author.name] = text
    with open("./bans.json", "w") as f:
        json.dump(data, f)
        await ctx.send("Text wurde gespeichert.")


bot.run("")