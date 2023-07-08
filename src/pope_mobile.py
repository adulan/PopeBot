import datetime, os
import discord
import actions, cardinal, constants, utils

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
    await utils.populate_cardinals(client.get_guild(constants.GUILD_ID))

# Define an event handler for when a message is sent in a channel
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # check if the message is a command
    if message.content.startswith("!"):
 
        if message.content.startswith("!Absolve"):
            # check if the author is a pope
            if not utils.author_is_pope(message):
                await message.reply("Only the Pope can absolve sins!")
                author = utils.get_cardinal_by_id(message.author.id)
                if author is not None:
                    author.add_sin_coins(25)
                    return
            
            # check if the message has a mention
            if len(message.mentions) > 0:
                user = message.mentions[0]
                await actions.absolve(user, message.channel)
            else:
                await message.reply("You need to mention someone to absolve them. Format: !Absolve @user")
        elif message.content.startswith("!Popeliness"):
            await actions.print_standings(message.channel)
        elif message.content.startswith("!Armageddon"):
            utils.armageddon = True
            await message.channel.send("Armageddon has begun.")
        elif message.content.startswith("!Rapture"):
            if utils.armageddon and utils.author_is_pope(message):
                await message.channel.send("Prepare for the Rapture!")
                # actions.rapture()
        elif message.content.startswith("!PP"):
            message_content = message.content.split(" ")
            # check if the message has two parameters
            if len(message_content) != 3:
                await message.reply("Format: !PP @user amount")
                return
                 # check if the message has a mention
            if len(message.mentions) > 0:
                user = message.mentions[0]
                cardinal = utils.get_cardinal_by_id(user.id)
                if cardinal is None:
                    print("Cardinal not found")
                    return
                
                # Get the number of points to add
                amount = message.content.split(" ")[2]
                # check if amount is a number
                if not amount.isdigit():
                    await message.reply("You need to enter a number. Format: !PP @user amount")
                else:
                    amount = int(amount)
                    cardinal.add_pope_points(amount)
            else:
                await message.reply("You need to mention someone to give them Pope Points. Format: !PP @user amount")
        elif message.content.startswith("!SC"):
            message_content = message.content.split(" ")
            # check if the message has two parameters
            if len(message_content) != 3:
                await message.reply("Format: !PP @user amount")
                return
            if len(message.mentions) > 0:
                user = message.mentions[0]
                cardinal = utils.get_cardinal_by_id(user.id)
                if cardinal is None:
                    print("Cardinal not found")
                    return
                
                # Get the number of points to add
                amount = message.content.split(" ")[2]
                # check if amount is a number
                if not amount.isdigit():
                    await message.reply("You need to enter a number. Format: !SC @user amount")
                else:
                    amount = int(amount)
                    cardinal.add_sin_coins(amount)
            else:
                await message.reply("You need to mention someone to give them Sin Coins. Format: !SC @user amount")
        elif message.content.startswith("!Cardinals"):
            #print size of cardinal list
            print("There are {0} cardinals.".format(len(utils.cardinal_list)))
            await message.channel.send("Cardinals:")
            for cardinal in utils.cardinal_list:
                list.append(f"{cardinal.name}: {cardinal.pope_points} Pope Points, {cardinal.sin_coins} Sin Coins\n")
            await message.channel.send(list)    
    
# Run the client with the Discord API token
client.run(os.environ.get("DISCORD_TOKEN"))