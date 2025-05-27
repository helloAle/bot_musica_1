import random
from discord.ext import commands, tasks
import discord
from discord import app_commands
import logging
import os
import asyncio
from dotenv import load_dotenv
import datetime
import sys

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!!", intents=discord.Intents.all(), application_id=int(os.getenv("BOT_ID")))

class SubButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = 600

@bot.event
async def on_ready(): 
    print(f"{bot.user} Online 🤖!")
    bot.loop.create_task(auto_shutdown())  # ✅ Inicia a task de desligamento automático

@bot.command()
@commands.is_owner() 
async def sync(ctx, guild=None):
    if guild is None:
        await bot.tree.sync()
    else:
        await bot.tree.sync(guild=discord.Object(id=int(guild)))
    await ctx.send("**Sincronizado!**", view=SubButton())

# ✅ Task que desliga o bot automaticamente em horário definido
async def auto_shutdown():
    while True:
        now = datetime.datetime.now()
        if now.hour == 00 and now.minute == 00:  # <-- 0horário aqui
            print("⏹️ Encerrando o bot automaticamente às 00:00.")
            await asyncio.sleep(1)
            sys.exit()
        await asyncio.sleep(60)

# ✅ Função principal que carrega os Cogs e inicia o bot
async def main():
    async with bot:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')

        TOKEN = os.getenv("DISCORD_TOKEN")
        await bot.start(TOKEN)

# 🔁 Roda o bot
asyncio.run(main())

#    _____                                            .___
#   / ___ \  _________________  ________    ____    __| _/
#  / / ._\ \/  ___/\___   /\  \/  /\__  \  /    \  / __ | 
# <  \_____/\___ \  /    /  >    <  / __ \|   |  \/ /_/ | 
#  \_____\ /____  >/_____ \/__/\_ \(____  /___|  /\____ | 
#               \/       \/      \/     \/     \/      \/ 