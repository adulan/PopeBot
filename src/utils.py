import cardinal, constants, discord


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