# Pope Bot

Pope Bot is made for Discord and allows users to give and receive Pope Points and Sin Coins to determine their Popeliness.

## Discord Permissions

To function fully, Pope Bot requires the `SERVER MEMBERS INTENT` and `MESSAGE CONTENT INTENT` Priviliged Gateway Intents

It also requires the following Bot Permissions

`Send Mesages`

`Manage Mesages`

`Use External Emojis`

`Add Reactions`

`Read Messages/View Channels`

## Run Locally

`docker build --pull --rm -f "Dockerfile" -t popebot:latest "."`

```
docker run -it \
--env DISCORD_TOKEN="YOUR_TOKEN" \
--env GUILD_ID="YOUR_SERVER_ID" \
--env POPELINESS_CHANNEL_ID="YOUR_CHANNEL_ID" \
--env HABEMUS_CHANNEL_ID="YOUR_CHANNEL_ID" \
--env ABSOLUTION_CHANNEL_ID="YOUR_CHANNEL_ID" \
--env POPE_ROLE_ID="YOUR_ROLE_ID" \
--rm --name pope_mobile.py popebot:latest
```

### Environment Variables
| Name | Required | Description |
| --- | --- |--- |
| DISCORD_TOKEN | Required | Discord > Applications > Bot > Token |
| GUILD_ID | Required | Discord Server ID |
| POPELINESS_CHANNEL_ID | Required | ID of the Server Channel to listen to for Point Point and Sin Coin grants
| HABEMUS_CHANNEL_ID | Required | ID of the Server Channel to perform Habemus Papam - Announcement of the new Pope
| ABSOLUTION_CHANNEL_ID | Required | ID of the Server Channel to listen to for Meme Absolutions
| POPE_ROLE_ID | Required | ID of the Server Role of the Pope


## Install from package

`$ docker pull ghcr.io/adulan/popebot:latest`

Update environment variables in docker-compose.yml then run

`$ docker compose up -d`