import datetime, discord
from constants import DISCORD_TOKEN
from utils import populate_cardinals
from actions import process_command
from bible_verses import check_reference

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


# Run the client with the Discord API token
client.run(DISCORD_TOKEN)
