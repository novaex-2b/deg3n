import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import grabber
import deg3n_scraper

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="#",intents=discord.Intents.all())
scraper = deg3n_scraper.deg3n_scraper()

@bot.event
async def on_ready():
    print(f"User: {bot.user} (ID: {bot.user.id})")
    if scraper is not None:
        await scraper.browser_setup()
        await scraper.page_setup()
        print("scraper is ready for use...")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == bot.user.id:
        return
    if any(link in message.content for link in ["/twitter.com/","/x.com/"]):
        embed_url = await scraper.twimg_parse(message.content)
        await message.reply(embed_url,mention_author=False)

@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send('Command tree synced!')

bot.run(TOKEN)
