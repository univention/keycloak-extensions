import requests


class KeycloakAPI:

    def __init__(self, base_url, realm):
        self.base_url = base_url
        self.realm = realm
        self.form = {
            "grant_type": "password",
            "client_id": "admin-cli",
            "realm": realm,
        }


    def get_oidc_token(self, username, password):
        r = requests.post(
            f'{self.base_url}/realms/{self.realm}/protocol/openid-connect/token',
            data={**{"username": username, "password": password}, **self.form}
        )
        return r
