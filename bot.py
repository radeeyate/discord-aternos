import discord
from python_aternos import Client, atserver, Lists
from dotenv import load_dotenv
import os
from query import get_info

load_dotenv()
TOKEN = os.getenv("TOKEN")
PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")
DOMAIN = os.getenv("DOMAIN")
ADMIN = os.getenv("ADMIN")
PREFIX = os.getenv("PREFIX")
print(USERNAME, PASSWORD)
at = Client.from_credentials(USERNAME, PASSWORD)
servers = at.list_servers()
for s in servers:
    print(s.subdomain)
    if s.domain == DOMAIN:
        serv = s
intents = discord.Intents.default()
intents.message_content = True
print(serv is None)

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f"{PREFIX}start"):
        serv.start()
        await message.channel.send(
            "Server Started! You might need to wait a minute for it start, be patient!"
        )
    elif message.content.startswith(f"{PREFIX}stop"):
        if message.author == ADMIN:
            serv.stop()
            await message.channel.send("Server Stopped!")
        else:
            await message.channel.send(
                "Server couldn't be stopped, you aren't an administrator!"
            )
    elif message.content.startswith(f"{PREFIX}restart"):
        if message.author == ADMIN:
            serv.restart()
            await message.channel.send("Server Restarted!")
        else:
            await message.channel.send(
                "Server couldn't be restarted, you aren't an administrator!"
            )
    elif message.content.startswith(f"{PREFIX}cancel"):
        serv.cancel()
        await message.channel.send("Server starting cancelled.")
    elif message.content.startswith(f"{PREFIX}info"):
        serv.fetch()
        await message.channel.send(
            f"""***{serv.domain}***
        Message of the Day: {serv.motd}
        Status: {serv.status}
        Full address: {serv.address}:{serv.port}
        Port: {str(serv.port)}
        Name: {serv.subdomain}
        Players online: {str(serv.players_count)} out of {str(serv.slots)}
        Minecraft: {serv.software} {serv.version}
        Is Bedrock: {str(serv.edition == atserver.Edition.bedrock)}
        Is Java: {str(serv.edition == atserver.Edition.java)}
                                """
        )
    elif message.content.startswith(f"{PREFIX}whitelist"):
        if message.author == ADMIN:
            if len(message.content) > 11:
                whitelist = serv.players(Lists.whl)
                whitelist.add(message.content[11:])
                await message.channel.send(
                    f"Added {message.content[11:]} to whitelist."
                )
            else:
                whitelist = serv.players(Lists.whl)
                await message.channel.send(whitelist.list_players())
        else:
            await message.channel.send("You aren't an admin!")
    elif message.content.startswith(f"{PREFIX}unwhitelist"):
        if message.author == ADMIN:
            whitelist = serv.players(Lists.whl)
            whitelist.remove(message.content[13:])
            await message.channel.send(
                f"Removed {message.content[13:]} from whitelist."
            )
        else:
            await message.channel.send("You aren't an admin!")
    elif message.content.startswith(f"{PREFIX}ban"):
        if message.author == ADMIN:
            serv.players(Lists.ban).add(message.content[5:])
            await message.channel.send(f"Banned {message.content[5:]}.")
        else:
            await message.channel.send("You aren't an admin!")
    elif message.content.startswith(f"{PREFIX}unban"):
        if message.author == ADMIN:
            serv.players(Lists.ban).remove(message.content[7:])
            await message.channel.send(f"Unbanned {message.content[7:]}.")
        else:
            await message.channel.send("You aren't an admin!")
    elif message.content.startswith(f"{PREFIX}op"):
        if message.author == ADMIN:
            serv.players(Lists.op).add(message.content[4:])
            await message.channel.send(f"OPed {message.content[4:]}.")
        else:
            await message.channel.send("You aren't an admin!")
    elif message.content.startswith(f"{PREFIX}deop"):
        if message.author == ADMIN:
            serv.players(Lists.op).remove(message.content[6:])
            await message.channel.send(f"DeOPed {message.content[6:]}.")
        else:
            await message.channel.send("You aren't an admin!")
    elif message.content.startswith(f"{PREFIX}players"):
        serv.fetch()
        if not serv.status == "offline":
            queryserver = get_info()["players"]["sample"]
            players = []
            for item in queryserver:
                players.append(item["name"])
            if not serv.players_count == 0:
                await message.channel.send(f"Players online: {', '.join(players)}")
            else:
                await message.channel.send("No players are currently online.")
        else:
            await message.channel.send("Server is offline.")

client.run(TOKEN)
c