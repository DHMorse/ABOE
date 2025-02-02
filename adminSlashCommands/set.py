import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import sqlite3

from const import COLORS, DATABASE_PATH # type: ignore
from helperFunctions.OE import updateXpAndCheckLevelUp # type: ignore

class AdminSet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="set", description="Set a stat for a user")
    @app_commands.checks.has_permissions(administrator=True)  # Restrict to admins
    async def adminSlashCommandSet(self, interaction: discord.Interaction, stat: str, value: str, member: discord.Member = None) -> None:
        if stat == '' or value == '':
            await interaction.response.send_message(f"```ansi\n{COLORS['red']}Please specify a stat and value to set.{COLORS['reset']}```", ephemeral=True)
            return
        
        stat = stat.lower().strip()

        if stat not in ['xp', 'money', 'lastLogin', 'loginStreak']:
            await interaction.response.send_message(f"```ansi\n{COLORS['red']}Please specify a valid stat to set it\'s value.{COLORS['reset']}```", ephemeral=True)
            await interaction.response.send_message(f'Valid stats: xp, money, lastLogin, loginStreak', ephemeral=True)
            return

        if stat == 'xp':
            try:
                value = int(value)
            except ValueError:
                await interaction.response.send_message(f"```ansi\n{COLORS['red']}Value\'s for xp must be integers.{COLORS['reset']}```", ephemeral=True)
                return
            
        if stat == 'money':
            try:
                value = float(value)
            except ValueError:
                await interaction.response.send_message(f"```ansi\n{COLORS['red']}Value\'s for money must be floats.{COLORS['reset']}```", ephemeral=True)
                return

        if member is None:
            member = interaction.author

        try:
            with sqlite3.connect(DATABASE_PATH) as conn:
                    cursor = conn.cursor()
                    match value:
                        case 'xp':
                            cursor.execute("SELECT xp FROM users WHERE userId = ?", (member.id,))
                            result = cursor.fetchone()
                            current_xp = result[0]
                            
                            if value > current_xp:
                                await updateXpAndCheckLevelUp(interaction, interaction.bot, value - current_xp, True)
                            elif value < current_xp:
                                await updateXpAndCheckLevelUp(interaction, interaction.bot, current_xp - value, False)

                            await interaction.response.send_message(f"```ansi\n{COLORS['blue']}Set {member.name}\'s xp to {value}.{COLORS['reset']}```", ephemeral=True)

                        case 'money':
                            cursor.execute("UPDATE users SET money = ? WHERE userId = ?", (value, member.id))
                            conn.commit()
                            await interaction.response.send_message(f"```ansi\n{COLORS['blue']}Set {member.name}\'s money to ${value}.{COLORS['reset']}```", ephemeral=True)

                        case 'lastLogin':
                            cursor.execute("UPDATE users SET lastLogin = ? WHERE userId = ?", (value, member.id))
                            conn.commit()
                            await interaction.response.send_message(f"```ansi\n{COLORS['blue']}Set {member.name}\'s last login to {value}.{COLORS['reset']}```", ephemeral=True)

                        case 'loginStreak':
                            cursor.execute("UPDATE users SET loginStreak = ? WHERE userId = ?", (value, member.id))
                            conn.commit()
                            await interaction.response.send_message(f"```ansi\n{COLORS['blue']}Set {member.name}\'s login streak to {value}.{COLORS['reset']}```", ephemeral=True)

                        case _:
                            await interaction.response.send_message(f"```ansi\n{COLORS['red']}Please specify a valid stat to set it\'s value.{COLORS['reset']}```", ephemeral=True)
                            await interaction.response.send_message(f'Valid stats: xp, money, lastLogin, loginStreak', ephemeral=True)
                            return
        except Exception as e:
            await interaction.response.send_message(f"```ansi\n{COLORS['red']}Error: {e}{COLORS['reset']}```", ephemeral=True)
            return

    @adminSlashCommandSet.error
    async def adminSlashCommandSetError(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminSet(bot))