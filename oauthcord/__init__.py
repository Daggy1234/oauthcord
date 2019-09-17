# Builtins
import requests

# Locals
from .application import Application
from .user import User

class App(object):
    """
    The main oauth class.
    """

    __slots__ = ("client_id", "client_secret", "scope", "redirect_uri", "discord_login_url", "discord_token_url", "discord_api_url", "user")

    def __init__(self, **kwargs):
        # Cache
        self.user = None

        # Discord Client Stuff
        self.client_id = kwargs.get("client_id")
        self.client_secret = kwargs.get("client_secret")
        self.scope = kwargs.get("scope")
        self.redirect_uri = kwargs.get("redirect_uri")

        # Discord base links
        #self.discord_login_url = "https://discordapp.com/api/oauth2/authorize?client_id={0.client_id}&redirect_uri={0.redirect_uri}&response_type=code&scope={0.scope}".format(self)
        self.discord_login_url = "https://discordapp.com/api/oauth2/authorize?client_id={0.client_id}&response_type=code&scope={0.scope}".format(self)
        self.discord_token_url = "https://discordapp.com/api/v6/oauth2/token"
        self.discord_api_url = "https://discordapp.com/api/v6"

    def get_login_url(self, form):
        """
        Get a login url with a redirect
        """
        return "https://discordapp.com/api/oauth2/authorize?client_id={0.client_id}&redirect_uri={1}&response_type=code&scope={0.scope}".format(self, form)

    def get_access_token(self, code, option=None):
        """
        Get a user's access token.
        Can be used to get user objects.
        """
        payload = {
            'client_id':self.client_id,
            'client_secret':self.client_secret,
            'grant_type': 'authorization_code',
            'code':code,
            'redirect_uri':self.redirect_uri,
            'scope':self.scope
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = requests.post(url=self.discord_token_url, data=payload, headers=headers)
        json = access_token.json()

        if "access_token" not in json.keys():
            return

        return json.get("access_token") if option is None else json.get(option)
    
    def refresh_token(self, refresh_token):
        """
        Refresh the token if the `expires_in` ends.
        """
        payload = {
            'client_id':self.client_id,
            'client_secret':self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token':refresh_token,
            'redirect_uri':self.redirect_uri,
            'scope':self.scope
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        res = requests.post(url=self.discord_token_url, data=payload, headers=headers)
        return res.json()
     
    def get_user(self, code):
        """
        Return the user object for an access token.
        """
        token_or_id = self.get_access_token(code)
        
        if isinstance(token_or_id, str):
            url = self.discord_api_url+"/users/@me"
            if "guild" in self.scope:
                url = self.discord_api_url+"users/@me/guilds"

            headers = {
                'Authorization': f"Bearer {token_or_id}"
            }

            user_object = requests.get(url=url, headers=headers)    
            user_json = user_object.json()
            id = user_json["id"]
            self.user = User(user_json)
            return User(user_json) if user_json.get("message") != "401: Unauthorized" else user_json
        else:
            return None
    
    def get_current_application(self, access_token):
        """
        Get current application.
        """
        url = self.discord_api_url+"oauth2/applications/@me"

        headers = {
            'Authorization': f"Bearer {access_token}"
        }

        application_object = requests.get(url=url, headers=headers)
        application_json = application_object.json()
        return Application(application_json) if application_json.get("message") != "401: Unauthorized" else application_json

# Make another class that inherits from oauthcord.User so that we can make a logout function
class UserLogout(User):
    def logout(self, session):
        """
        Logs out the user
        """
        try:
            self.user = None
        except Exception as error:
            return error