import time

import jwt
from decouple import config


JWT_SECRET = config("SECRET")
JWT_ALGORITHM = config("ALGORITHM")


def token_response(token: str):
    return {
        "token": token
    }


def signJWT(user_id: str) -> dict[str, str]:
    payload = {
        "email": user_id,
        "expires": time.time() + 6000
    }
    encoded = jwt.encode(payload, JWT_SECRET,
                         algorithm="HS256").decode("utf-8")
    return token_response(encoded)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithm=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
