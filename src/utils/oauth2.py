import typing as tp

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


def get_file_by_path(path: str):
    try:
        with open(path, 'r') as f:
            key = f.read()
        return key
    except:
        return '123'


class Settings(BaseModel):
    authjwt_algorithm: str = 'HS256'
    authjwt_decode_algorithms: tp.List = ['HS256']
    authjwt_token_location: set = {'cookies'}
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_secret_key: str = get_file_by_path('~/Diplom/keys/SECRET_KEY')


@AuthJWT.load_config
def get_config():
    return Settings()
