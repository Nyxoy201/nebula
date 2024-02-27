EMBED_CONFIG = {
    "title": "",    # Maine Embed Title here 
    "description": "",   # Main Embed Description here 
    "color": 0xFF5733,   # Change embed color if you want (red)
    "fields": [
        {"name": "test", "value": "test", "inline": False},    # Embed Field → Juste Modify → Just edit the empty places
        {"name": "test", "value": "test", "inline": False},
        {"name": "test","value": "test", "inline": False},    # Exemple → "name": "Title 1", "value": "Hello, here is my message", "inline": False
    ],
    "image": "",   # Embed Icon url here → https://image.jpg
    "footer": "",  # Embed Footer here 
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

BOT_PRESENCE = {
    "type": "playing",  # "playing", "listening", or "watching"
    "text": "Nebula"  # Your text presence
}
