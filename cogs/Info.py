import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command
import os
from datetime import timedelta

currency = "DKC"

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def emb(self, title, description):
        return(
            nextcord.Embed(
                title=title,
                description=description,
                colour=nextcord.Color.dark_gold())
                .set_footer(text=f"Bot author - {os.getenv('BOT_AUTHOR')}"))
 
    @nextcord.slash_command(name="ping", description="Pokes the bot and shows the ping")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(embed=self.emb(f"Ping is {round(self.bot.latency * 1000)}ms", "The bot is online!"))


    @nextcord.slash_command(name="help", description="Displays all commands")
    async def help(self, interaction: Interaction):
        embed = nextcord.Embed(title=f"Commands", description=f"List of all commands", color=nextcord.Color.dark_gold())
        embed.add_field(name="Info", value=f"""
        help - Displays all commands
        ping - Pokes the bot and shows the ping
        user - Shows info about a user
        botinfo - Shows info about the bot""", inline=False)

        embed.add_field(name="Gamble", value=f"""
        slots - Play slots with {currency}
        coinflip - Flip a coin with {currency}
        dice - Roll a dice with {currency}""", inline=False)

        embed.add_field(name="Economy", value=f"""
        send - Send a person some {currency}
        balance - Check someones balance
        leaderboard - Check top 10 balances
        hourly - Hourly {currency}
        daily - Daily {currency}
        hack - Hack something and get {currency}""", inline=False)

        embed.add_field(name="Moderation", value=f"""
        purge - Purge amount of messages
        ban - Ban a user
        kick - Kick a user""", inline=False)
        
        embed.add_field(name="Fun", value=f"""
        8ball - Ask a question and get an answer""", inline=False)
        embed.set_footer(text=f"Bot author - {os.getenv('BOT_AUTHOR')}")
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="botinfo", description="Shows info about the bot")
    async def botinfo(self, interaction: Interaction):
        embed = nextcord.Embed(title=f"{self.bot.user}", description=f"{self.bot.user.mention}", color=nextcord.Color.dark_gold())
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.add_field(name="Bot creator:", value=f"`KING CRIMSON#0101`", inline=False)
        embed.add_field(name="Bot creator ID:", value=f"`190028486444843009`", inline=False)
        embed.add_field(name="Bot is in:", value=f"`{len(self.bot.guilds)} servers`", inline=False)
        embed.add_field(name="Total members using the bot:", value=f"`{len(self.bot.users)}`", inline=False)
        embed.set_footer(text=f"Bot author - {os.getenv('BOT_AUTHOR')}")
        
        await interaction.response.send_message(embed=embed)
    

    @nextcord.slash_command(name="user", description="Shows info about a user")
    async def user(self, interaction: Interaction, user: nextcord.User):

        embed = nextcord.Embed(title=f"{user}", description=f"{user.mention}", color=nextcord.Color.dark_gold())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User ID:", value=f"`{user.id}`", inline=False)
        try:
            embed.set_image(url=user.banner.url)
        except AttributeError:
            pass
        try:
            embed.add_field(name="Activity:", value=f"`{user.activity.name}`", inline=False)
        except AttributeError:
            pass
        try:
            embed.add_field(name="Status:", value=f"{user.status.name}", inline=False)
        except AttributeError:
            pass
        try:
            embed.add_field(name="Top role:", value=f"`{user.top_role}` / `{user.top_role.mention}`", inline=False)
        except AttributeError:
            pass
        try:
            embed.add_field(name="Is bot:", value=f"`{user.bot}`", inline=True)
        except AttributeError:
            pass

        embed.add_field(name="Created at:", value=f"`{user.created_at.strftime('%Y/%m/%d')}`", inline=True)
        try:
            embed.add_field(name="Joined at:", value=f"`{user.joined_at.strftime('%Y/%m/%d')}`", inline=True)
        except AttributeError:
            pass
        embed.set_footer(text=f"Bot author - {os.getenv('BOT_AUTHOR')}")
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))