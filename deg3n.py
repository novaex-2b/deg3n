import discord
from discord.ext import commands
from discord import app_commands
import os,re
from dotenv import load_dotenv
from twscrape import API

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="#",intents=discord.Intents.all())
api = None

@bot.event
async def on_ready():
    print(f"User: {bot.user} (ID: {bot.user.id})")
    api = API()
    await api.pool.login_all()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == bot.user.id:
        return

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=discord.Object(id=1177961540377395292))
    await ctx.send('Command tree synced!')

@bot.tree.command(name="deg3n",guild=discord.Object(id=1177961540377395292))
async def deg3n(interaction: discord.Interaction, url: str):
    tweetid = int(re.search("[\d]+$",url).group())
    tweet_info = await api.tweet_details(tweetid)
    twimg_url = details.media.photos[0].url
    await interaction.response.send_message(content=twimg_url,allowed_mentions=None)

bot.run(TOKEN)
