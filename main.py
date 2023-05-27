import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, SlashOption
from dotenv import load_dotenv
import os
import cooldowns
from cooldowns import CallableOnCooldown
from random import randint
from random import choice as rchoice
from datetime import timedelta
import pymongo

load_dotenv()

currency = "DKC"
client = pymongo.MongoClient(os.getenv("MONGO_TOKEN"))
db = client.users

def emb(title, description):
    return(
        nextcord.Embed(
            title=title,
            description=description,
            colour=nextcord.Color.dark_gold())
            .set_footer(text=f"Bot author - {os.getenv('BOT_AUTHOR')}"))


intents = nextcord.Intents.all()
intents.members = True

activity = nextcord.Activity(type=nextcord.ActivityType.listening, name=f"/help")
bot = commands.Bot(command_prefix="/", intents=intents, activity=activity)

def createWallet(id):
    if db.userbal.find_one({"id": id}) == None:
        db.userbal.insert_one({"id": id, "balance": 5000})
    else:
        pass

def getBalance(id):
    createWallet(id)
    find_user = db.userbal.find({"id": id})
    for u in find_user:
        return u["balance"]

def AddBalance(id, add):
    updated_user_bal = getBalance(id) + add
    db.userbal.update_one({"id": id}, {"$set": {"balance": updated_user_bal}})

def RemoveBalance(id, remove):
    updated_user_bal = getBalance(id) - remove
    db.userbal.update_one({"id": id}, {"$set": {"balance": updated_user_bal}})

@bot.event
async def on_ready():
    print(f"{bot.user}")
    print(f"{bot.user.id}")
    print(f"BOT IN {len(bot.guilds)} SERVERS, WITH {len(bot.users)} USERS TOTAL\n\n")
    print(f"{db}\n\n")

@bot.slash_command(name="balance", description=f"Check someones balance")
async def balance(interaction: nextcord.Interaction, user: nextcord.User):
    bal = getBalance(user.id)
    await interaction.response.send_message(embed=emb(f"{user} balance", f"{user.mention} balance is `{bal}` {currency}"))

@bot.slash_command(name="leaderboard", description=f"Check top 5 balances leaderbord")
async def leaderboard(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="Top 5 ballers", description=f"", color=nextcord.Color.dark_gold())
    spot = 0 
    for u in db.userbal.find().sort("balance", -1).limit(5):
        spot += 1
        leadername = u["id"]
        leaderbal = u["balance"]
        embed.add_field(name=f"Top {spot}", value=f"<@{leadername}> - `{leaderbal}` {currency}", inline=False)
    embed.set_footer(text=f"Bot author - {os.getenv('BOT_AUTHOR')}")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="slots", description=f"Play slots with {currency}")
@cooldowns.cooldown(1, 2, bucket=cooldowns.SlashBucket.author)
async def slots(interaction: nextcord.Interaction, bet: int):
    if bet >= 1 and getBalance(interaction.user.id) >= bet:
        pass
    else:
        await interaction.response.send_message(embed=emb(f"Please check your balance", f"")) 

    slots_selection = [':cherries:', ':grapes:', ':gem:', ':coin:']
    slots_row_1_col_1 = slots_selection[randint(0, 3)]
    slots_row_1_col_2 = slots_selection[randint(0, 3)]
    slots_row_1_col_3 = slots_selection[randint(0, 3)]

    slots_row_2_col_1 = slots_selection[randint(0, 3)]
    slots_row_2_col_2 = slots_selection[randint(0, 3)]
    slots_row_2_col_3 = slots_selection[randint(0, 3)]

    slots_row_3_col_1 = slots_selection[randint(0, 3)]
    slots_row_3_col_2 = slots_selection[randint(0, 3)]
    slots_row_3_col_3 = slots_selection[randint(0, 3)]

    res1 = await interaction.response.send_message(embed=emb(f"Slots - Rolling", f"""| :purple_square: | :purple_square: | :purple_square: |\n| :purple_square: | :purple_square: | :purple_square: |\n| :purple_square: | :purple_square: | :purple_square: |"""))

    await res1.edit(embed=emb(f"Slots - Rolling", f"""| {slots_row_1_col_1} | {slots_row_1_col_2} | {slots_row_1_col_3} |\n| :purple_square: | :purple_square: | :purple_square: |\n| :purple_square: | :purple_square: | :purple_square: |"""))

    await res1.edit(embed=emb(f"Slots - Rolling", f"""| {slots_row_1_col_1} | {slots_row_1_col_2} | {slots_row_1_col_3} |\n| {slots_row_2_col_1} | {slots_row_2_col_2} | {slots_row_2_col_3} |\n| :purple_square: | :purple_square: | :purple_square: |"""))

    await res1.edit(embed=emb(f"Slots - Calculating", f"""| {slots_row_1_col_1} | {slots_row_1_col_2} | {slots_row_1_col_3} |\n| {slots_row_2_col_1} | {slots_row_2_col_2} | {slots_row_2_col_3} |\n| {slots_row_3_col_1} | {slots_row_3_col_2} | {slots_row_3_col_3} |"""))

    if slots_row_1_col_1 == slots_row_1_col_2 == slots_row_1_col_3:
        winning = int(bet) * 4
        win = True
    elif slots_row_2_col_1 == slots_row_2_col_2 == slots_row_2_col_3:
        winning = int(bet) * 4
        win = True
    elif slots_row_3_col_1 == slots_row_3_col_2 == slots_row_3_col_3:
        winning = int(bet) * 4
        win = True
    elif slots_row_1_col_1 == slots_row_1_col_2 == slots_row_1_col_3 == slots_row_2_col_1 == slots_row_2_col_2 == slots_row_2_col_3:
        winning = int(bet) * 15
        win = True
    elif slots_row_2_col_1 == slots_row_2_col_2 == slots_row_2_col_3 == slots_row_3_col_1 == slots_row_3_col_2 == slots_row_3_col_3:
        winning = int(bet) * 15
        win = True
    elif slots_row_1_col_1 == slots_row_1_col_2 == slots_row_1_col_3 == slots_row_2_col_1 == slots_row_2_col_2 == slots_row_2_col_3 == slots_row_3_col_1 == slots_row_3_col_2 == slots_row_3_col_3:
        winning = int(bet) * 120
        win = True
    else:
        winning = 0
        win = False

    if win == True:
        AddBalance(interaction.user.id, winning)
        await res1.edit(embed=emb(f"Slots - You :regional_indicator_w:on +{winning} {currency}", f"""| {slots_row_1_col_1} | {slots_row_1_col_2} | {slots_row_1_col_3} |\n| {slots_row_2_col_1} | {slots_row_2_col_2} | {slots_row_2_col_3} |\n| {slots_row_3_col_1} | {slots_row_3_col_2} | {slots_row_3_col_3} |\n\n{interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}"""))
    else:
        RemoveBalance(interaction.user.id, bet)
        await res1.edit(embed=emb(f"Slots - You :regional_indicator_l:ost -{bet} {currency}", f"""| {slots_row_1_col_1} | {slots_row_1_col_2} | {slots_row_1_col_3} |\n| {slots_row_2_col_1} | {slots_row_2_col_2} | {slots_row_2_col_3} |\n| {slots_row_3_col_1} | {slots_row_3_col_2} | {slots_row_3_col_3} |\n\n{interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}"""))


@bot.slash_command(name="coinflip", description=f"Flip a coin with {currency}")
async def coinflip(interaction: nextcord.Interaction, bet: int, choice: str = SlashOption(choices=["Heads","Tails"], required=True)):
    if bet >= 1 and getBalance(interaction.user.id) >= bet:
        pass
    else:
        await interaction.response.send_message(embed=emb(f"Please check your balance", f""))

    headtails = ["Heads", "Tails"]
    cf = rchoice(headtails)
    if choice == cf:
        AddBalance(interaction.user.id, bet)
        await interaction.response.send_message(embed=emb(f"Coinflip - {cf} - You :regional_indicator_w:on +{bet} {currency}", f"{interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}"))
    else:
        RemoveBalance(interaction.user.id, bet)
        await interaction.response.send_message(embed=emb(f"Coinflip - {cf} - You :regional_indicator_l:ost -{bet} {currency}", f"{interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}"))

@bot.slash_command(name="dice", description=f"Roll a dice with {currency}")
async def rolldice(interaction: nextcord.Interaction, bet: int, choice: int = SlashOption(choices=[1,2,3,4,5,6], required=True)):
    if bet >= 1 and getBalance(interaction.user.id) >= bet:
        pass
    else:
        await interaction.response.send_message(embed=emb(f"Please check your balance", f"")) 
    
    randomdiceroll = randint(1,6)
    if choice == randomdiceroll:
        dicewinning = bet * 3
        AddBalance(interaction.user.id, dicewinning)
        await interaction.response.send_message(embed=emb(f"Dice rolled {randomdiceroll} - You :regional_indicator_w:on +{dicewinning} {currency}", f"{interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}"))
    else:
        RemoveBalance(interaction.user.id, bet)
        await interaction.response.send_message(embed=emb(f"Dice rolled {randomdiceroll} - You :regional_indicator_l:ost -{bet} {currency}", f"{interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}"))

@bot.slash_command(name="send", description=f"Send a person some {currency}")
async def send(interaction: nextcord.Interaction, user: nextcord.User, amount: int):
    if user.id is not interaction.user.id and getBalance(interaction.user.id) >= amount and amount >= 1:
        RemoveBalance(interaction.user.id, amount)
        AddBalance(user.id, amount)
        await interaction.response.send_message(embed=emb(f"You sent `{amount}` {currency} to {user.name}#{user.discriminator}", f"""
        {interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}
        {user.mention} current balance is `{getBalance(user.id)}` {currency}"""))
    else:
        await interaction.response.send_message(embed=emb(f"You can't send {currency} to {user.name}#{user.discriminator}", f"Please check your balance"))

@bot.slash_command(name="hourly", description=f"Hourly {currency}")
@cooldowns.cooldown(1, 3600, bucket=cooldowns.SlashBucket.author)
async def hourly(interaction: nextcord.Interaction):
    hourly_bal = randint(5000, 10000)
    AddBalance(interaction.user.id, hourly_bal)
    await interaction.response.send_message(embed=emb(f"You got `{hourly_bal}` {currency} from hourly", f"{interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}"))

@bot.slash_command(name="daily", description=f"Daily {currency}")
@cooldowns.cooldown(1, 86400, bucket=cooldowns.SlashBucket.author)
async def hourly(interaction: nextcord.Interaction):
    daily_bal = randint(50000, 100000)
    AddBalance(interaction.user.id, daily_bal)
    await interaction.response.send_message(embed=emb(f"You got `{daily_bal}` {currency} from daily", f"{interaction.user.mention} current balance is `{getBalance(interaction.user.id)}` {currency}"))

@bot.slash_command(name="hack", description=f"Hack something and get {currency}")
@cooldowns.cooldown(1, 1800, bucket=cooldowns.SlashBucket.author)
async def hack(interaction: nextcord.Interaction):
    diffrent_hacks_msg = [
    'hacked the goverment and earned',
    'hacked the FBI and earned',
    'hacked the Europol and earned',
    'hacked the presidents bank account and earned',
    'hacked the CIA and earned',
    'hacked the police departament and earned',
    'hacked the IRS and earned',
    'hacked Google and earned',
    'hacked Youtube and earned',
    'hacked Twitch and earned',
    'hacked Discord and earned',
    'hacked Walter White and earned',
    'hacked a bank and earned',
    'hacked a charity and earned',
    'hacked a normal citizen and earned',
    'hacked a cryptocurrency and earned',
    'hacked a police officer and earned',
    'hacked a bank truck and earned',
    'hacked a friend and earned',
    'hacked a government official and earned',
    'hacked a businessman and earned',
    'hacked a corrupt policeman and earned',
    'hacked a school and earned',
    'hacked a university and earned',
    'hacked a neighbour and earned',
    'hacked a hacker and earned',
    'hacked a cartel and earned'
    ]

    caughtmanmsg = [
    'FBI',
    'CIA',
    'police',
    'government',
    'IRS',
    'DHS',
    'DOJ',
    'KGB',
    'ENISA',
    'EDA',
    'Europol',
    'EBA',
    'eu-LISA'
    ]

    randomhackmsg = rchoice(diffrent_hacks_msg)
    randomcaught = rchoice(caughtmanmsg)
    earned = randint(1, 2500000)
    hacksucc = randint(1, 17)
    hackfail = randomhackmsg.replace(" and earned", "")

    if hacksucc == 1:
        AddBalance(interaction.user.id, earned)
        await interaction.response.send_message(embed=emb(title=f"YO HOW?", description=f"{interaction.user.mention} {randomhackmsg} `{earned}` {currency}"))

    elif hacksucc != 1:
        await interaction.response.send_message(embed=emb(title=f"Unlucky...", description=f"{interaction.user.mention} {hackfail}, but got caught by the {randomcaught}"))


@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    error = getattr(error, "original", error)
    if isinstance(error, CallableOnCooldown):
        await interaction.response.send_message(embed=emb(f"You are on cooldown", f"Retry in `{error.retry_after}` seconds"))
    else:
        raise error

for filename in os.listdir("cogs/"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv("BOT_TOKEN"))