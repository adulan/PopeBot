import datetime, discord
from constants import DISCORD_TOKEN
from utils import populate_cardinals
from actions import process_command

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


# Run the client with the Discord API token
client.run(DISCORD_TOKEN)

# python -m coverage run -m unittest tests.test_actions tests.test_cardinal tests.test_utils
# python -m coverage report 
# echo $(python -c "import xml.etree.ElementTree as ET; root = ET.parse('coverage.xml').getroot(); print(root.attrib['line-rate'])")
