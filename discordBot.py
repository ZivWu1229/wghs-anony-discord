import discord
from discord.ext import commands

import Get_Post

intents = discord.Intents.all()
client=  commands.Bot(command_prefix="/",intents=intents)

@client.event
async def on_ready():
    print("Bot online!")

@client.command()
async def ping(ctx):
    await ctx.message.author.send(ctx.message.author.id)

@client.command()
async def login(ctx):
    pass

@client.command()
async def logout(ctx):
    pass

@client.command()
async def GetPost(ctx):
    post=Get_Post.Post()
    post.get_post()
    await ctx.message.author.send(post.text)

client.run('ODU2MzM3OTc1NTQ4NzA2ODM2.GJ6O2o.oLcTPCWcBK9xlDrRPyVJR7YZsHo5EFUcBXtcks')