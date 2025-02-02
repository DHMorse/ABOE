import discord
from discord import app_commands
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="admin_command", description="This command is only for admins")
    @app_commands.checks.has_permissions(administrator=True)  # Restrict to admins
    async def admin_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("You are an admin!", ephemeral=True)

    @admin_command.error
    async def admin_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
