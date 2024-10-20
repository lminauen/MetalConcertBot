import discord

from openai_utils import get_response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import get_past_dates, write_log

from config import DISCORD_BOT_TOKEN, DISCORD_USER_ID, INTERESTS

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

scheduler = AsyncIOScheduler()

# On connecting
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # Schedule regular check for sunday morning
    scheduler.add_job(regular_check, 'cron', day_of_week='sun', hour=9, minute=30)


# Responding to DMs
@client.event
async def on_message(message):
    # Don't respond to self
    if message.author == client.user:
        return
    # Only respond to DMs
    if isinstance(message.channel, discord.DMChannel):
        response = get_response(message.content)
        # Empty messages not allowed by discord
        if response:
            await message.channel.send(response)
    return

# Scheduled query
async def regular_check():
    user = await client.fetch_user(DISCORD_USER_ID)
    if user:
        try:
            write_log("Executing scheduled query.", "System")

            bands_string = ", ".join(INTERESTS)
            query = "Please check google for new concert announcements of the past week, from " + get_past_dates(7) + ". Focus on the following bands: " + bands_string
            write_log(query, "System")

            response = get_response(query)
            write_log(response, "OpenAI")

            await user.send(response)
        except discord.Forbidden:
            write_log("Cannot send message to user.", "System")
    else:
        write_log("User not found.", "System")

client.run(DISCORD_BOT_TOKEN)

