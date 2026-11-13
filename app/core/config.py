from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env', env_file_encoding='utf-8')

    mongo_url: str = 'mongodb://localhost:27017'
    mongo_db: str = 'test_db'

    redis_url: str = 'redis://localhost:6379/0'
    cache_ttl: int = 60

    rabbit_url: str = 'amqp://guest:guest@localhost:5672/'

    celery_result_backend: str = 'redis://localhost:6379/1'

    yandex_client_id: str | None = None
    yandex_client_secret: SecretStr | None = None
    yandex_redirect_uri: str = 'http://localhost:8000/auth/yandex/callback'
    yandex_oauth_url: str = 'https://oauth.yandex.ru'
    yandex_login_url: str = 'https://login.yandex.ru'

    yandex_disk_token: SecretStr | None = None
    yandex_disk_url: str = 'https://cloud-api.yandex.net'

    #YandexGPT


settings = Settings()
