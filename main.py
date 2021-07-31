import discord
from discord.ext import commands, tasks
import re
from keep_alive import keep_alive
import json
import os
import timestamp 
import asyncio
from itertools import cycle
import random
import datetime
if os.path.exists(os.getcwd() + "/config.json"):
    
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "1"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 

prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")



print('Starting...')
print('Loading Commands')
print('Commands Loaded')
print('Server Active')
client = discord.Client()
client.command = bot.command
bot.command =client.command
@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help CursedBots.inc ©2021"))
    
    
@bot.command(description="Gets the bot's latency.")
async def ping(ctx):
    latency = round(bot.latency * 100, 1)
    await ctx.send(f"The gateway ping for Server Admin is  {latency}ms")

@bot.command()
async def hi(ctx, member):
    await ctx.send(f"Hello! {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} was banned!")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} was kicked!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discriminator = member.split("#")

    for ban in bannedUsers:
        user = ban.user

        if(user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} was unbanned.")
            return

@bot.command()
@commands.has_permissions(administrator=True)
async def activity(ctx, *, activity):
    await bot.change_presence(activity=discord.Game(name=activity))
    await ctx.send(f"Bot's activity changed to {activity}")


@bot.command()
async def userinfo(ctx):
    user = ctx.author

    embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx, commandSent=None):
    if commandSent != None:

        for command in bot.commands:
            if commandSent.lower() == command.name.lower():

                paramString = ""

                for param in command.clean_params:
                    paramString += param + ", "

                paramString = paramString[:-2]

                if len(command.clean_params) == 0:
                    paramString = "None"
                    
                embed=discord.Embed(title=f"HELP - {command.name}", description=command.description)
                embed.add_field(name="parameters", value=paramString)
                await ctx.message.delete()
                await ctx.author.send(embed=embed)
        
    else:
        embed=discord.Embed(title="Help")
        embed.add_field(name="ping", value="Gets the bots latency", inline=True)
        embed.add_field(name="hi", value="Says hello to a specified user, Parameters: Member", inline=True)
        embed.add_field(name="userinfo", value="Retreives info about the user", inline=True)

        await ctx.message.delete()
        await ctx.author.send(embed=embed)

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

@bot.command(description="repeats the specified message every specified seconds")
async def repeatmessage(ctx, enabled="start", interval=10, message=""):
    if enabled.lower() == "stop":
        messageInterval.cancel()
    elif enabled.lower() == "start":
        messageInterval.change_interval(seconds=int(interval))
        messageInterval.start(ctx, message)

@tasks.loop(seconds=10)
async def messageInterval(ctx, message):
    await ctx.send(message)

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
  

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are missing the Manage Messages Permission please contact an Administrator!")


@bot.command()
async def GoodBye(ctx):
    await ctx.send("I have been requested to leave by my owner GoodBye!")
    await ctx.guild.leave()






@bot.command(aliases=["mc"])

async def member_count(ctx):

    a=ctx.guild.member_count
    b=discord.Embed(title=f"members in {ctx.guild.name}",description=a,color=discord.Color((0x00FFE5)))
    await ctx.send(embed=b)

mainshop = [{"name":"Watch","price":100,"description":"Time"},
        {"name":"Laptop","price":1000,"description":"Work"},
        {"name":"PC","price":10000,"description":"Gaming"},
        {"name":"Ferrari","price":99999,"description":"Sports Car"},
        {"name":"Rich","price":99999999,"description":"Rich"},{"name":"Dildo","price":10,"description":"I swear it's not mine!"},
        {"name":"Lambo","price":100000,"description":"Nice car!"},
        {"name":"McLaren","price":500000,"description":"Designer car"},
        {"name":"Tesla","price":1000000,"description":"Electric car"},
        {"name":"Bently","price":9000000,"description":"Rich mans car"},{"name":"CursedBots.inc employee tag","price":300,"description":"Cursed"},{"name":"Bugatti","price":10000000,"description":'Stupidly Expensive'}]




@bot.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{ctx.author.name} Balance',color = discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)

@bot.command()
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f'{ctx.author.mention} Got {earnings} Bitcoin!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)


@bot.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} Bitcoin')


@bot.command(aliases=['dp'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You deposited {amount} Bitcoin')


@bot.command(aliases=['sm'])
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount,'bank')
    await update_bank(member,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} Bitcoin')

@bot.command(aliases=['rb'])
async def rob(ctx,member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)


    if bal[0]<10:
        await ctx.send('It is useless to rob him :(')
        return

    earning = random.randrange(0,bal[0])

    await update_bank(ctx.author,earning)
    await update_bank(member,-1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} Bitcoin')

@bot.command()
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['X','O','Q'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send(f'You won :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f'You lose :( {ctx.author.mention}')

@bot.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)


@bot.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough Bitcoin in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@bot.command()
async def inv(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Inventory")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

@bot.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = bot.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True


async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal

@bot.command()
async def work(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(1001)

    await ctx.send(f'{ctx.author.mention} Got {earnings} Bitcoin!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)

@bot.command()
async def addmoney(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(99999999)

    await ctx.send(f'{ctx.author.mention} Got {earnings} Bitcoin!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)

    return


@bot.command()
async def owneronly(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(99999999999999999999999999999999999999999999999999999)

    await ctx.send(f'{ctx.author.mention} Got {earnings} Bitcoin!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)

    return



keep_alive()
my_secret = os.environ['Token']
bot.run (my_secret)
