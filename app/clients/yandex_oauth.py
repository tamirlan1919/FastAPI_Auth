import logging
from urllib.parse import urlencode

import httpx

from app.schemas.yandex import YandexProfile, YandexToken


logger = logging.getLogger(__name__)

class YandexOauthError(Exception):
    pass



class YandexOauthClient:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            oauth_url: str = 'https://accounts.yandex.com',
            login_url: str = 'https://accounts.yandex.com',
            timeout: float = 5.0,
            transport: httpx.AsyncBaseTransport | None = None,

    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.oauth_url = oauth_url
        self.login_url = login_url
        self._client = httpx.AsyncClient(timeout=timeout, transport=transport)

    async def aclose(self):
        await self._client.aclose()

    def authorize(self, state: str) -> str:
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': state,
        }
        return f'{self.oauth_url}/authorize?{urlencode(params)}'


    async def exchange_code(self, code: str) -> YandexToken:
        try:
            response = await self._client.post(
                f'{self.oauth_url}/token',
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                }
            )
        except httpx.TransportError as e:
            raise YandexOauthError(f'Яндекс Oauth недоступен')

        if response.status_code != 200:
            logger.warning('Обмен кода не удался')
            raise YandexOauthError(response.json()['error_description'])
        return YandexToken.model_validate(response.json())


    async def get_profile(self, access_token: str) -> YandexProfile:
        try:
            response = await self._client.get(
                f'{self.login_url}/info',
                params={'format': 'json'},
                headers={'Authorization': f'Oauth {access_token}'},
            )
        except httpx.TransportError as e:
            raise YandexOauthError('Яндекс ID недоступен')

        if response.status_code != 200:
            logger.warning('Профиль не получен')
            raise YandexOauthError('Яндекс ID упал')
        return YandexProfile(**response.json())

