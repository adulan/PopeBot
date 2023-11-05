import datetime, discord
from constants import DISCORD_TOKEN
from utils import populate_cardinals
from actions import process_command
from bible_verses import check_reference
from social_media import replace_instagam_link, replace_tiktok_link, replace_twitter_link


# Define the Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)


# Define an event handler for when the client connects to Discord
@client.event
async def on_ready():
    print("Logged in as {0.user}.".format(client))
    print(datetime.datetime.now())
    await populate_cardinals(client)


# Define an event handler for when a message is sent in a channel
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # check if the message is a command
    if message.content.startswith("!"):
        await process_command(message, client)

    # check if the message is a bible reference
    reference = check_reference(message.content)
    if reference != False:
        await message.channel.send(reference)

    # Check if social media link
    content = message.content.lower()
    if content.find("://www.instagram.com") >= 0:
        await replace_instagam_link(message)
    elif content.find("://www.tiktok.com") >= 0:
        await replace_tiktok_link(message)
    elif content.find("://www.twitter.com") >= 0:
        await replace_twitter_link(message)


# Run the client with the Discord API token
client.run(DISCORD_TOKEN)
