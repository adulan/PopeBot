from utils import cardinal_list


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
    cardinal_list.sort(key=lambda x: x.popeliness(), reverse=True)
    
    for cardinal in cardinal_list:
        standings.append("{0}: {1}".format(cardinal.name, cardinal.popeliness()))
    
    # Join the standings with newlines
    standings = "\n".join(standings)
    await channel.send(standings)