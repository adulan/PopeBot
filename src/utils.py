import cardinal, constants
import discord


cardinal_list = []
armageddon = False

def author_is_pope(message):
    author = message.author
    return member_has_role(author, constants.POPE_ROLE_ID)


async def populate_cardinals(guild):
    try:
        members = guild.members
        cardinal_role = guild.get_role(constants.CARDINAL_ROLE_ID)
    except:
        print("Error: Could not get members from guild")
        return
    for member in members:
        cardinal_list.append(cardinal.Cardinal(member))
        print(f"Added {member.name} to cardinal_list")
        
        if cardinal_role is not None:
            try:
                if not member_has_role(member, cardinal_role.id):
                    await member.add_roles(cardinal_role)
                    print(f"Assigned {member.name} to Cardinals Role")
            except discord.DiscordException as e:
                print(f"Error: Could not assign {member.name} to Cardinals Role")
                print(e)
            
    print("Cardinals populated.")


def get_cardinal_by_id(id):
    for cardinal in cardinal_list:
        if cardinal.id == id:
            return cardinal
    return None


def member_has_role(member, role_id):
    try:
        roles = member.roles
    except:
        print("Error: Could not get roles from member")
        return False

    for member_role in roles:
        if member_role.id == role_id:
            return True
    return False

def rank_cardinals():
    global cardinal_list
    ranks = cardinal_list
    #Rank cardinals by popeliness. Break ties with lowest amt of sin_coins
    ranks.sort(key=lambda x: (x.popeliness(), -1*x.sin_coins), reverse=True)
    return ranks

def get_pope():
    for cardinal in cardinal_list:
        if member_has_role(cardinal.member, constants.POPE_ROLE_ID):
            return cardinal
    return None

async def check_for_pope_change(client):
    print("Checking for pope change")
    current_pope = get_pope()
    if current_pope is None:
        print("Current pope is None")
        ranked_cardinals = rank_cardinals()
        first_place = ranked_cardinals[0]
        print(f"First place is {first_place.name}")
        await set_pope(first_place.member, None)
    else:
        print(f"Current pope is {current_pope.name}")
        ranked_cardinals = rank_cardinals()
        first_place = ranked_cardinals[0]
        if first_place != current_pope:
            await set_pope(first_place.member, current_pope.member, client)
    return True
        

async def set_pope(new_pope, old_pope, client):
    pope_changed = False
    try:
        pope_role = client.get_guild(constants.GUILD_ID).get_role(constants.POPE_ROLE_ID)
        await new_pope.add_roles(pope_role)
        if old_pope is not None:
            await old_pope.remove_roles(pope_role)
        pope_changed = True
        await announce_pope_change(new_pope, client)
    except discord.DiscordException as e:
        print("Error: Could not set pope role")
        print(e)
    return pope_changed

async def announce_pope_change(member, client):
    try:
        channel = client.get_channel(constants.ANNOUNCEMENT_CHANNEL_ID)
        await channel.send(f"{member.mention} is the new pope!")
    except discord.DiscordException as e:
        print("Error: Could not announce pope change")
        print(e)
        