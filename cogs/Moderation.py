import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command
import os

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def emb(self, title, description):
        return(
            nextcord.Embed(
                title=title,
                description=description,
                colour=nextcord.Color.dark_gold())
                .set_footer(text=f"Bot author - {os.getenv('BOT_AUTHOR')}"))


    @nextcord.slash_command(name="purge", description="Purge amount of messages")
    @application_checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: nextcord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        purgedmsg = await interaction.response.send_message(embed=self.emb(f"Successfully purged {amount} messages!", f""))
        await purgedmsg.delete(delay=2)

    @nextcord.slash_command(name="ban", description="Ban a user")
    @application_checks.has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, user: nextcord.User, reason: str):
        await user.ban(reason=reason, delete_message_days=0)
        await interaction.response.send_message(embed=self.emb(f"{user.mention} has been banned for {reason}", f""))

    @nextcord.slash_command(name="kick", description="Kick a user")
    @application_checks.has_permissions(kick_members=True)
    async def kick(self, interaction: nextcord.Interaction, user: nextcord.User, reason: str):
        await user.kick(reason=reason)
        await interaction.response.send_message(embed=self.emb(f"{user.mention} has been kicked for {reason}", f""))

def setup(bot):
    bot.add_cog(Moderation(bot))