import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def 어시스턴트(callbot):
    await callbot.send('네')

bot.run('MTA1MDA0MDMwNDcwMDQ4OTc0OA.GWEj08.QVUODXc9XeA2mMOB7dqCncBilGMiRVEXXEOQFo')