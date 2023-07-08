import cardinal, constants, discord


cardinal_list = []

def author_is_pope(message):
    isPope = False
    author_roles = message.author.roles
    for role in author_roles:
        if role.id == constants.POPE_ROLE_ID:
            isPope = True
    return isPope

async def populate_cardinals(guild):
    try:
        members = guild.members
    except:
        print("Error: Could not get members from guild")
        return
    for member in members:
        cardinal_list.append(cardinal.Cardinal(member))
        print(f"Added {member.name} to cardinal_list")
    print("Cardinals populated.")

def get_cardinal_by_id(id):
    for cardinal in cardinal_list:
        if cardinal.id == id:
            return cardinal
    return None
