import os


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

LISTENING_CHANNEL_ID = int(os.getenv("POPELINESS_CHANNEL_ID"))
ANNOUNCEMENT_CHANNEL_ID = int(os.getenv("HABEMUS_CHANNEL_ID"))
ABSOLUTION_CHANNEL_ID = int(os.getenv("ABSOLUTION_CHANNEL_ID"))

POPE_ROLE_ID = int(os.getenv("POPE_ROLE_ID"))
CARDINAL_ROLE_ID = int(os.getenv("CARDINAL_ROLE_ID")) if os.getenv("CARDINAL_ROLE_ID") is not None else None

CARDINAL_LIST_FILE = "/usr/src/app/cardinal_list.json"
WHITE_SMOKE_FILE = "/usr/src/app/images/white_smoke.jpg"
BLACK_SMOKE_FILE = "/usr/src/app/images/black_smoke.jpg"
HABEMUS_IMAGE_FILE = "/usr/src/app/images/habemus_papam.png"