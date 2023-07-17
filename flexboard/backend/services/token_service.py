from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from config import config_object


class TokenService:
    # https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#__tabbed_1_2:~:text=the%20same%20time.-,Hash%20and%20verify%20the%20passwords,-%C2%B6
    # This was not created by me. From Documentation.
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        :param data: the payload that will be encoded.
        :param expires_delta: the expiry value for the encoded token that will be produced. If none given, a default will be given.
        """
        payload_to_encode: dict = data.copy()

        if expires_delta:
            expire: datetime = datetime.utcnow() + expires_delta
        else:
            expire: datetime = datetime.utcnow() + timedelta(
                minutes=int(config_object.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

        # Update the dictionary key, "exp" with the expiry value.
        payload_to_encode.update({"exp": expire})

        encoded_jwt: str = jwt.encode(
            payload_to_encode,
            config_object.JWT_SECRET_KEY,
            algorithm=config_object.JWT_ALGORITHM
        )

        return encoded_jwt


token_service: TokenService = TokenService()
