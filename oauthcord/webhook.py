# Packages
import requests, aiohttp

# Locals
from .user import User

class Webhook(object):
    """
    Webhook object
    """

    __slots__ = ("name", "id", "channel_id", "guild_id", "user", "token")

    def __init__(self, payload=None):
        # Webhook info
        self.name = payload.get("name")
        self.id = payload.get("id")

        # Context
        self.channel_id = payload.get("channel_id")
        self.guild_id = payload.get("guild_id")

        # User object
        self.user = User(dict=payload.get("user"))

        # Token
        self.token = payload.get("token")
    
    def delete(self):
        """Delete the webhook"""
        if self.token is not None:
            ret = requests.delete(f"https://discordapp.com/webhooks/{id}")
        else:
            ret = requests.delete(f"https://discordapp.com/webhooks/{id}/{token}")
        return ret

class WebhookHandler:
    """
    Holds webhook methods
    """

    __slots__ = ("url", "username", "avatar_url", "content")

    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.username = kwargs.get("username")
        self.avatar_url = kwargs.get("avatar_url")
        self.content = kwargs.get("content")
    
    def send(self, payload=None) -> "response code":
        """
        Send a webhook to a channel. 

        Payload can either be a string or a dictionary, if made a string it will send that content using the predefined class variables. If it is a dict it will use those values.
        
        Payload keys
        ---
        `username` : Requires a string for the webhook username
        `avatar_url` : Requires a string for the webhook avatar url
        `content` : Requires a string for the message content
        """
        if payload is None:
            values = {
                "url": self.url,
                "username": self.username,
                "avatar_url": self.avatar_url,
                "content": self.content
            }
            try:
                ret = requests.post(self.url, json=payload)
            except Exception as error:
                raise error
        elif isinstance(payload, dict):
            url = payload.get("url") if self.url is None else self.url
            try:
                ret = requests.post(self.url, json=payload)
            except Exception as error:
                raise error
            return Webhook(payload=ret.json())
        elif isinstance(payload, str):
            values = {
            } 
            values["username"] = "None" if self.username is None else self.username
            if self.avatar_url is not None: values["avatar_url"] = self.avatar_url
            values["content"] = payload
            try:
                ret = requests.post(self.url, json=values)
            except Exception as error:
                raise error
            return Webhook(payload=ret.json())
    
    def delete_webhook(self, **kwargs):
        id = kwargs.get("id")
        token = kwargs.get("token")
        if token is not None and id is None:
            raise ValueError("Nedd a webhook id for deleting webhook with token")
        if token is not None:
            ret = requests.delete(f"https://discordapp.com/webhooks/{id}")
        else:
            ret = requests.delete(f"https://discordapp.com/webhooks/{id}/{token}")
        return ret

    def get_channel_webhooks(self, channel_id):
        """
        Get the webhooks for a certain channel using the channel id
        """
        ret = requests.get(f"https://discordapp.com/channels/{channel_id}/webhooks")
        return ret
    
    def get_guild_webhooks(self, guild_id):
        """
        Get the webhooks for a certain guild using the guild id
        """
        ret = requests.get(f"https://discordapp.com/guilds/{guild_id}/webhooks")
        return ret
    
    def get_webhook(self, webhook_id):
        """
        Get a webhook using a webhook's id
        """
        ret = requests.get(f"https://discordapp.com/webhooks/{webhook_id}")
        return ret

class AsyncWebhookHandler:
    """
    Holds Async Webhook methods
    """

    __slots__ = ("url", "username", "avatar_url", "content")

    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.username = kwargs.get("username")
        self.avatar_url = kwargs.get("avatar_url")
        self.content = kwargs.get("content")
    
    async def send(self, payload=None) -> "response code":
        """
        Send a webhook to a channel. 

        Payload can either be a string or a dictionary, if made a string it will send that content using the predefined class variables. If it is a dict it will use those values.
        
        Payload keys
        ---
        `username` : Requires a string for the webhook username
        `avatar_url` : Requires a string for the webhook avatar url
        `content` : Requires a string for the message content
        """
        if payload is None:
            values = {
                "url": self.url,
                "username": self.username,
                "avatar_url": self.avatar_url,
                "content": self.content
            }
            try:
                ret = await aiohttp.post(self.url, json=payload)
            except Exception as error:
                raise error
        elif isinstance(payload, dict):
            url = payload.get("url") if self.url is None else self.url
            try:
                ret = await aiohttp.post(self.url, json=payload)
            except Exception as error:
                raise error
            return Webhook(payload=ret.json())
        elif isinstance(payload, str):
            values = {
            } 
            values["username"] = "None" if self.username is None else self.username
            if self.avatar_url is not None: values["avatar_url"] = self.avatar_url
            values["content"] = payload
            try:
                ret = await aiohttp.post(self.url, json=values)
            except Exception as error:
                raise error
            return Webhook(payload=ret.json())
    
    async def delete_webhook(self, **kwargs):
        id = kwargs.get("id")
        token = kwargs.get("token")
        if token is not None and id is None:
            raise ValueError("Nedd a webhook id for deleting webhook with token")
        if token is not None:
            ret = await aiohttp.delete(f"https://discordapp.com/webhooks/{id}")
        else:
            ret = await aiohttp.delete(f"https://discordapp.com/webhooks/{id}/{token}")
        return ret

    async def get_channel_webhooks(self, channel_id):
        """
        Get the webhooks for a certain channel using the channel id
        """
        ret = await aiohttp.get(f"https://discordapp.com/channels/{channel_id}/webhooks")
        return ret
    
    async def get_guild_webhooks(self, guild_id):
        """
        Get the webhooks for a certain guild using the guild id
        """
        ret = await aiohttp.get(f"https://discordapp.com/guilds/{guild_id}/webhooks")
        return ret
    
    async def get_webhook(self, webhook_id):
        """
        Get a webhook using a webhook's id
        """
        ret = await aiohttp.get(f"https://discordapp.com/webhooks/{webhook_id}")
        return ret

