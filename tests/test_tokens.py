import pytest

from src.domains import TokenType, User, Token
from src.tokens import create_jwt_token
import jwt


def test_create_jwt_access_token(given_private_pem, given_public_pem):
    # given
    given_payload = {"user_name": "sangjae", "user_group": "haimp-developer"}

    # when
    access_token = create_jwt_token(given_payload, TokenType.ACCESS, given_private_pem, 10)

    # then
    payload = jwt.decode(access_token, given_public_pem, algorithms=["RS256"])

    assert payload["type"] == "access"
    assert payload["user_name"] == "sangjae"
    assert payload["user_group"] == "haimp-developer"


def test_create_jwt_refresh_token(given_private_pem, given_public_pem):
    # given
    given_payload = {}

    # when
    access_token = create_jwt_token(given_payload, TokenType.REFRESH, given_private_pem, 10)

    # then
    payload = jwt.decode(access_token, given_public_pem, algorithms=["RS256"])

    assert payload["type"] == "refresh"


def test_create_jwt_token_expired_case(given_private_pem, given_public_pem):
    # given
    given_payload = {"user_name": "sangjae", "user_group": "haimp-developer"}

    # when
    access_token = create_jwt_token(given_payload, TokenType.ACCESS, given_private_pem, -10)

    # then
    with pytest.raises(jwt.exceptions.ExpiredSignatureError):
        jwt.decode(access_token, given_public_pem, algorithms=["RS256"])


def test_generate_token(given_token_generator, given_public_pem):
    # user
    user = User(
        name='sangjae',
        role='admin',
        group='haimp-developer'
    )

    token = given_token_generator.generate_token(user)

    assert isinstance(token, Token)

    access_payload = jwt.decode(token.access, given_public_pem, algorithms=['RS256'])
    refresh_payload = jwt.decode(token.refresh, given_public_pem, algorithms=['RS256'])

    assert access_payload['exp'] < refresh_payload['exp']
