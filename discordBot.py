import discord
from discord.ext import commands

from json import loads,dumps
from os import listdir
from os.path import abspath

import Get_Post
from auto_split import split as auto_split

intents = discord.Intents.all()
client=  commands.Bot(command_prefix="/",intents=intents)

users={}
posts={}
users_file='users.json'
help_text=\
'''
/ping                  :就是這個頁面
/login                 :登入(每次進來都先打一下)
/get                    :顯示投稿文字
/set+文字         :將貼文文字改為輸入的文字(用於手動換行)
/split                  :自動換行
/skip                   :略過貼文
/number+編號:設定貼文編號
/number           :顯示貼文編號
/draw                 :繪製貼文
/approve           :批准貼文
/deny                 :駁回貼文
以上指令建議在私聊打(伺服器也行就是很麻煩)
'''

#read users info
with open(users_file,'r') as file:
    users=loads(file.read())
def save_users():
    with open(users_file,'w') as file:
        file.write(dumps(users))

@client.event
async def on_ready():
    print("Bot online!")

@client.command()
async def ping(ctx):
    await ctx.message.author.send(help_text)

@client.command()
async def login(ctx,email=None,pwd=None):
    id=ctx.message.author.id
    if users.get(id):
        await ctx.message.author.send("You already logged in. Go ahead!")
        return
    code=1
    posts[id]=Get_Post.Post()
    try:
        if email and pwd:
            await ctx.message.author.send("Logging in...\nPlease Wait...")
            code=posts[id].login({"email":email,"password":pwd})
        elif users.get(str(id)):
            await ctx.message.author.send("Logging in...\nPlease Wait...")
            code=posts[id].login(users[str(id)])
        else:
            #posts[id].logout()
            await ctx.message.author.send("Who are you? Try /login [email] [password]")
            return
    except:
        posts[id].logout()
        await ctx.message.author.send("Error occurred while logging in. Contact Ziv Wu.")
    else:
        if code==1:
            posts[id].logout()
            await ctx.message.author.send("Log in failed.")
        else:
            if email and pwd:
                users[id]={}
                users[id]['email']=email
                users[id]['password']=pwd
            save_users()
            await ctx.message.author.send(f"Log in success!\nWelcome, {code}")
            print(code+" logged in.")


@client.command()
async def get(ctx):
    id=ctx.message.author.id
    if not posts.get(id):
        await ctx.message.author.send("You aren't logged in. Type /login to log in.")
        return 
    post=posts[id]
    #post.get_post()
    await ctx.message.author.send(post.text)

@client.command()
async def set(ctx,*arg):
    id=ctx.message.author.id
    if not posts.get(id):
        await ctx.message.author.send("You aren't logged in. Type /login to log in.")
        return 
    post=posts[id]
    post.text=' '.join(arg)
    await ctx.message.author.send("Text is set to "+post.text)

@client.command()
async def refresh(ctx):
    id=ctx.message.author.id
    if not posts.get(id):
        await ctx.message.author.send("You aren't logged in. Type /login to log in.")
        return 
    post=posts[id]
    post.get_post()
    await ctx.message.author.send(post.text)

@client.command()
async def split(ctx):
    id=ctx.message.author.id
    post=posts[id]
    post.text=auto_split(post.text)
    await ctx.message.author.send(post.text)

@client.command()
async def skip(ctx):
    id=ctx.message.author.id
    post=posts[id]
    post.skip()
    await ctx.message.author.send(post.text)

@client.command()
async def number(ctx,number=None):
    if number:
        try:
            users["number"]=int(number)
            
        except:
            await ctx.message.author.send("Invalid number!")
        else:
            save_users()
            await ctx.message.author.send("Post number is set to "+str(users["number"]))
    else:
        await ctx.message.author.send(users["number"])

@client.command()
async def draw(ctx):
    id=ctx.message.author.id
    post=posts[id]
    post.number=users["number"]
    post.submit()
    for i in listdir(abspath('output')):
        await ctx.message.author.send(file=discord.File(abspath('output/'+i)))

@client.command()
async def approve(ctx):
    id=ctx.message.author.id
    post=posts[id]
    #text=post.get_post()
    post.approve()
    users['number']+=1
    save_users()
    await ctx.message.author.send("Post approved!")

@client.command()
async def deny(ctx):
    id=ctx.message.author.id
    post=posts[id]
    #text=post.get_post()
    post.ban()
    await ctx.message.author.send("Post denied!")

@client.command()
async def logout(ctx):
    id=ctx.message.author.id
    posts[id].logout()
    del posts[id]


client.run('MTI3OTM4MTkwMzE0NDY1Mjg3MA.GiFac3.PWtV19zdKj2j-khSo3T7yCcf1s19SGJIxwToVw')