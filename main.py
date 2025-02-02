import discord
from discord import app_commands
from discord.ext import commands
import time
from dotenv import load_dotenv
import os

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def setup_hook(self):
        # Load command files dynamically from adminSlashCommands
        for file in os.listdir("./adminSlashCommands"):
            if file.endswith(".py") and file != "__init__.py":
                await self.load_extension(f"adminSlashCommands.{file[:-3]}")
        
        # Sync commands globally
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    botTreeSyncStartTime = time.time()
    await bot.tree.sync()
    print(f'Bot tree sync took {round(time.time() - botTreeSyncStartTime, 2)} seconds')
    print(f'Bot is ready. Logged in as {bot.user}')

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)
