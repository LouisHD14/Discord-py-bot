import discord

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print ("Booting up your system")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)
    
bot.run("MTAzODQ2MDQxODk0OTEyNDIxOA.GiAjxe.MPWrPf1MUDvrecl-HoLn9dbc7RWUDpfZUOAVno")
