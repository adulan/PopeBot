import discord
from utils import cardinal_list, armageddon, author_is_pope, set_mention_cardinals, \
    get_cardinal_by_id, populate_cardinals_json, rank_cardinals, check_for_pope_change, save_cardinals_json
from constants import GUILD_ID, CARDINAL_ROLE_ID


# Function that sets the given user's sin_coins to 0
async def absolve(user, channel):
    id = user.id
    for cardinal in cardinal_list:
        if cardinal.id == id:
            cardinal.sin_coins = 0
            await channel.send(f"<@{id}>, You have been absolved of all your sins!")
            return

# Create a message that prints out the current standings
async def print_standings(channel):
    # Create a list of strings that will be printed
    embed = discord.Embed(description="The current Cardinals of the Vatican")
    cardinal_ranks = rank_cardinals()
    
    if len(cardinal_ranks) > 0:
        fields = [("Cardinals", "\n".join([f"{cardinal.name}: {cardinal.popeliness()}" for cardinal in cardinal_ranks]), False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await channel.send(embed=embed)


async def print_cardinals(channel):
    embed = discord.Embed(description="The current Cardinals of the Vatican")
    
    if len(cardinal_list) > 0:
        fields = [("Cardinals", "\n".join([f"{cardinal.name}: {cardinal.pope_points}, {cardinal.sin_coins} " for cardinal in cardinal_list]), False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await channel.send(embed=embed)


async def process_command(message, client):
    global armageddon
    message_content = message.content.split(" ")
    message_command = message_content[0].upper()

    match message_command:
        case "!ABSOLVE":
            # check if the author is a pope
            if not author_is_pope(message):
                await message.reply("Only the Pope can absolve sins!")
                author = get_cardinal_by_id(message.author.id)
                if author is not None:
                    author.add_sin_coins(25)
                return
            
            # check if the message has a mention
            if len(message.mentions) > 0:
                user = message.mentions[0]
                await absolve(user, message.channel)
                await check_for_pope_change(client)
            else:
                await message.reply("You need to mention someone to absolve them. Format: !Absolve @user")
        
        case "!POPELINESS":
            await print_standings(message.channel)
        
        case "!ARMAGEDDON":
            armageddon = True
            await message.channel.send("Armageddon has begun.")
        
        case "!RAPTURE":
            if armageddon and author_is_pope(message):
                await message.channel.send("Prepare for the Rapture!")
                # actions.rapture()
                armageddon = False
            else:
                print("Error: Armageddon has not begun or author is not a pope")

        case "!PP":
            # check if the message has two parameters
            if len(message_content) != 3:
                await message.reply("Format: !PP @user amount")
                return
            # check if the message has a mention
            if len(message.mentions) > 0:
                user = message.mentions[0]
                cardinal = get_cardinal_by_id(user.id)
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
                    await check_for_pope_change(client)
            else:
                await message.reply("You need to mention someone to give them Pope Points. Format: !PP @user amount")

        case "!SC":
            # check if the message has two parameters
            if len(message_content) != 3:
                await message.reply("Format: !SC @user amount")
                return
            if len(message.mentions) > 0:
                user = message.mentions[0]
                cardinal = get_cardinal_by_id(user.id)
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
                    await check_for_pope_change(client)
            else:
                await message.reply("You need to mention someone to give them Sin Coins. Format: !SC @user amount")
    
        case "!CARDINALS":
            await print_cardinals(message.channel)

        case "!SAVE":
            saved = save_cardinals_json()
            if saved:
                await message.reply("Cardinals saved")

        case "!LOAD":
            guild = client.get_guild(GUILD_ID)
            
            # Require double confirmation to load Cardinals
            channel_history = [message async for message in message.channel.history(limit=2)]
            if len(channel_history) == 2:
                previous_message = channel_history[1]
                if previous_message.content.upper() == "!LOAD" and message.author.id != previous_message.author.id:
                    if populate_cardinals_json(guild):
                        await message.reply("Cardinals loaded")
                    else:
                        print("Error: Could not load Cardinals")
                else:
                    print("Need two members to load Cardinals")

        case "!HELP":
            fields = []
            fields.append(["!PP @user ##", "Give pope points to user", False])
            fields.append(["!SC @user ##", "Give sin coins to user", False])
            fields.append(["!PopeLiness", "Prints the current standings of the Cardinals", False])
            fields.append(["!Absolve @user", "The Pope may Absolve user of all sins", False])
            fields.append(["!Save", "Save the current Cardinals to a JSON file", False])
            fields.append(["!Mention [True|False]", "Sets mentioning Cardinals during Habemus Papam", False])
            fields.append(["!Help", "Prints this message", False])

            embed = discord.Embed(description="Commands")
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            await message.channel.send(embed=embed)

        case "!MENTION":
            if len(message_content) != 2:
                await message.reply("Format: !Mention [True|False]")
                return
            if message_content[1].upper() == "TRUE" and CARDINAL_ROLE_ID is not None:
                set_mention_cardinals(True)
                print("Mentioning Cardinals during Habemus Papam")
            else:
                set_mention_cardinals(False)
                print("Habemus Papam will not mention Cardinals")