from utils import cardinal_list, armageddon, author_is_pope, get_cardinal_by_id, rank_cardinals, check_for_pope_change


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
    standings = []
    cardinal_ranks = rank_cardinals()
    
    for cardinal in cardinal_ranks:
        standings.append("{0}: {1}".format(cardinal.name, cardinal.popeliness()))
    
    # Join the standings with newlines
    standings = "\n".join(standings)
    await channel.send(standings)

async def print_cardinals(channel):
    output = []
    await channel.send("Cardinals:")
    for cardinal in cardinal_list:
        output.append(f"{cardinal.name}")
    output = "\n".join(output)
    await channel.send(output)

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
                await message.reply("Format: !PP @user amount")
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