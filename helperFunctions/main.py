import discord

async def missingPermissionsHandler(interaction: discord.Interaction):
    await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)