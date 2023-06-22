import datetime, os
import discord


# Define the Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Define an event handler for when the client connects to Discord
@client.event
async def on_ready():
    print("Logged in as {0.user}.".format(client))
    print(datetime.datetime.now())

# Define an event handler for when a message is sent in a channel
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
# Run the client with the Discord API token
client.run(os.environ.get("DISCORD_TOKEN"))