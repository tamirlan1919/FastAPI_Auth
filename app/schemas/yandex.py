from pydantic import BaseModel


class YandexToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None


class YandexProfile(BaseModel):
    id: int
    login: str
    display_name: str | None = None
    real_name: str | None = None
    default_email: str | None = None
    default_avatar_id: str | None = None
    is_avatar_empty: bool = True


    @property
    def avatar_url(self):
        if self.is_avatar_empty or not self.default_avatar_id:
            return None
        return f'https://avatars.yandex.net/get-yapic/{self.default_avatar_id}/islands-200'





class DiskLine(BaseModel):
    href: str
    method: str
    templated: bool = False


class DiskUploadOut(BaseModel):
    path: str
    public_url: str

