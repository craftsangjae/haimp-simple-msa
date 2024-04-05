from typing import Dict

import jwt

from src.domains import User, Token, TokenType
from datetime import datetime


class TokenGenerator:
    """ Jwt Token을 생성합니다.
    """

    def __init__(
        self,
        private_key: bytes,
        access_token_lifetime: int = 86400,  # 하루
        refresh_token_lifetime: int = 2592000,  # 한달
    ):
        self.private_key = private_key
        self.access_token_lifetime = access_token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime

    def generate_token(self, user: User) -> Token:
        """Token을 생성합니다.
        :param user:
        :return:
        """
        # access token 만들기
        access = create_jwt_token(
            user.to_dict(),
            TokenType.ACCESS,
            self.private_key,
            self.access_token_lifetime,
        )

        # refresh token 만들기
        refresh = create_jwt_token(
            {}, TokenType.REFRESH, self.private_key, self.refresh_token_lifetime
        )

        return Token(access=access, refresh=refresh)


def create_jwt_token(payload: Dict, type: TokenType, private_key: bytes, lifetime: int) -> str:
    """JWT 토큰을 생성합니다."""
    return jwt.encode(
        {**payload, "type": type.value, "exp": datetime.now().timestamp() + lifetime},
        private_key,
        algorithm="RS256",
    )
