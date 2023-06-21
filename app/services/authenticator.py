import requests
import discord


class Authenticator:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

    def generate_discord_oauth_url(self):
        """
        Generates the Discord OAuth URL.

        :return: The Discord OAuth URL.
        """
        return f'https://discord.com/api/oauth2/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}'

    def exchange_authorization_code_for_access_token(self, code):
        """
        Exchanges the authorization code for an access token.

        :param code: The authorization code.
        :return: The access token.
        """
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(
            'https://discord.com/api/oauth2/token', data=data, headers=headers)

        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(
                'Failed to exchange authorization code for access token')

    def get_discord_profile_info(self, access_token):
        """
        Retrieves the user's Discord profile information.

        :param access_token: The access token.
        :return: The user's Discord profile information.
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(
            'https://discord.com/api/users/@me', headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to retrieve Discord profile information')
