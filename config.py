import os

# General
LOGGING = True

LOCATION = os.getenv('LOCATION')
RANGE = "2 hours"

# Discord Bot
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Google API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

# OpenAI
MODEL = "gpt-4o"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Interests
INTERESTS = [
    "Beast in Black",
    "Ghost",
    "Delain",
    "Dynazty",
    "Battle Beast",
    "Visions of Atlantis",
    "Illumishade",
    "Wind Rose",
    "Powerwolf",
    "Alestorm",
    "Korpiklaani",
    "Nocturna",
    "Rammstein",
    "Rise Against",
    "Disturbed",
    "Linkin Park",
    "Feuerschwanz",
    "Brothers of Metal",
    "Arion",
    "Orden Ogan",
    "Avantasia",
    "Sabaton",
    "The Raven Age",
    "The Offspring",
    "Within Temptation",
    "Caleb Hyles",
    "Frozen Crown",
    "Eluveitie",
    "Xandria",
    "Nightwish",
    "Eclipse",
    "Amaranthe",
    "Bloodbound"
]
