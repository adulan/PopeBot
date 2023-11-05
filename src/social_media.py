async def replace_instagam_link(message):
    content = message.content.lower()
    new_msg = content.replace("://www.instagram.com", "://www.ddinstagram.com")
    author = message.author.display_name
    new_msg = "f{author} posted a link to Instagram: {new_msg}"
    await message.channel.send(new_msg)
    await message.delete()

async def replace_tiktok_link(message):
    content = message.content.lower()
    new_msg = content.replace("://www.tiktok.com", "://www.vxtiktok.com")
    author = message.author.display_name
    new_msg = "f{author} posted a link to TikTok: {new_msg}"
    await message.channel.send(new_msg)
    await message.delete()

async def replace_twitter_link(message):
    content = message.content.lower()
    new_msg = content.replace("://www.twitter.com", "://www.fxtwitter.com")
    author = message.author.display_name
    new_msg = "f{author} posted a link to Twitter: {new_msg}"
    await message.channel.send(new_msg)
    await message.delete()