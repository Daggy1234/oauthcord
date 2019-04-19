# Import the WebhookHandler class
from oauthcord.webhook import WebhookHandler, AsyncWebhookHandler

#===== USING PRESET USERNAME, AVATAR_URL AND CONTENT =====#

# Make a basic WebhookHandler class
webhook = WebhookHandler(url="URL", username="username", avatar_url="avatar url", content="content")

# Sends whatever WebhookHandler.content was given as to the WebhookHandler.url
webhook.send()

#===== NOT USING PRESET USERNAME, AVATAR_URL AND CONTENT =====#

# Make a basic WebhookHandler class
webhook = WebhookHandler(url="URL")

# Sends the webhook to WebhookHandler.url, note that it will still look for what you specified when making the App, so you can specify username and avatar_url and only put content.
webhook.send({
    "username": "username",
    "avatar_url": "avatar_url",
    "content": "content"
})

#===== ASYNCHRONOUS VERSION =====#

# The AsyncWebhookHandler class is exactly the same as the WebhookHandler, just asynchronous.
webhook = WebhookHandler(url="URL", username="username", avatar_url="avatar url", content="content")

# Sends whatever AsyncWebhookHandler.content was given as to the AsyncWebhookHandler.url
async def func():
    await webhook.send()

#===== NOT USING PRESET USERNAME, AVATAR_URL AND CONTENT =====#

# Make a basic WebhookHandler class
webhook = AsyncWebhookHandler(url="URL")

# Sends the webhook to AsyncWebhookHandler.url, note that it will still look for what you specified when making the App, so you can specify username and avatar_url and only put content.
async def func():
    await webhook.send({
        "username": "username",
        "avatar_url": "avatar_url",
        "content": "content"
    })