import discord

from openai_utils import get_response

from config import DISCORD_BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# On connecting
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

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

client.run(DISCORD_BOT_TOKEN)
