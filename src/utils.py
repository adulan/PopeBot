import cardinal, constants
import discord, json, os


cardinal_list = []
armageddon = False

def author_is_pope(message):
    author = message.author
    return member_has_role(author, constants.POPE_ROLE_ID)


async def populate_cardinals(client):
    global cardinal_list
    guild = client.get_guild(constants.GUILD_ID)
    # if CARDINAL_LIST_FILE exists, populate from json
    if os.path.isfile(constants.CARDINAL_LIST_FILE):
        populate_cardinals_json(guild)
        await check_for_pope_change(client)
    else:
        print("No cardinal_list.json found. Populating from guild.")
    # Continue to populate from guild
    try:
        members = guild.members
        cardinal_role = guild.get_role(constants.CARDINAL_ROLE_ID)
    except:
        print("Error: Could not get members from guild")
        return
    for member in members:
        # if member id does not match any cardinal id, add to cardinal_list
        cur_cardinal = get_member_from_cardinal_list(member)
        if cur_cardinal is None:
            cardinal_list.append(cardinal.Cardinal(member))
            print(f"Added {member.name} to cardinal_list")
        else:
            print(f"{member.name} already in cardinal_list")
        
        if cardinal_role is not None:
            try:
                if not member_has_role(member, cardinal_role.id):
                    await member.add_roles(cardinal_role)
                    print(f"Assigned {member.name} to Cardinals Role")
            except discord.DiscordException as e:
                print(f"Error: Could not assign {member.name} to Cardinals Role")
                print(e)
            
    print("Cardinals populated.")

# Populate cardinals from json file
def populate_cardinals_json(guild):
    global cardinal_list
    try:
        with open(constants.CARDINAL_LIST_FILE, "r") as f:
            cardinal_json = json.load(f)
            f.close()
        for element in cardinal_json:
            print(element)
            member = guild.get_member(element["id"])
            cur_cardinal = cardinal.Cardinal(member)
            cur_cardinal.from_json(element)
            cardinal_list.append(cur_cardinal)
        print("Cardinals populated from json.")
    except Exception as e:
        print("Error: Could not populate cardinals from json.")
        print(e)


# Save cardinals in cardinal_list to json file
def save_cardinals_json():
    global cardinal_list
    cardinal_json = []
    for cardinal in cardinal_list:
        cardinal_json.append(cardinal.to_json())
    try:
        with open(constants.CARDINAL_LIST_FILE, "w") as f:
            json.dump(cardinal_json, f)
            f.close()
        print("Cardinals saved.")
    except:
        print("Error: Could not save cardinals.")


def get_cardinal_by_id(id):
    global cardinal_list
    for cardinal in cardinal_list:
        if cardinal.id == id:
            return cardinal
    return None


def get_member_from_cardinal_list(member):
    global cardinal_list
    for cardinal in cardinal_list:
        if cardinal.id == member.id:
            return member
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
    current_pope = get_pope()
    if current_pope is None:
        ranked_cardinals = rank_cardinals()
        first_place = ranked_cardinals[0]
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
        save_cardinals_json()
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
        