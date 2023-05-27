import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command
import random
from random import choice
import os

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def emb(self, title, description):
        return(
            nextcord.Embed(
                title=title,
                description=description,
                colour=nextcord.Color.dark_gold())
                .set_footer(text=f"Bot author - {os.getenv('BOT_AUTHOR')}"))


    @nextcord.slash_command(name="8ball", description="Ask a question and get an answer")
    async def _8ball(self, interaction: nextcord.Interaction, question: str):
        eballresponses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "Bot reply is no.",
            "Bot sources say no.",
            "Outlook not so good.",
            "Very doubtful."]

        await interaction.response.send_message(embed=self.emb(f"{question}", f"{random.choice(eballresponses)}"))


def setup(bot):
    bot.add_cog(Fun(bot))