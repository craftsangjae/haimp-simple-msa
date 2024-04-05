import pytest

from src.domains import User, TokenType
from src.exceptions import InvalidTokenException


def test_domain_user_to_dict():
    given_user = User("sj", "admin", "haimp-developer")

    user_data = given_user.to_dict()

    assert user_data['user_name'] == 'sj'
    assert user_data['user_role'] == 'admin'
    assert user_data['user_group'] == 'haimp-developer'


def test_domain_user_from_dict():
    given_user = User.from_dict({
        "user_name": "sj",
        "user_role": "admin",
        "user_group": "haimp-developer"
    })

    assert given_user.name == 'sj'
    assert given_user.role == 'admin'
    assert given_user.group == 'haimp-developer'


def test_token_type_from_text():
    assert TokenType.from_text("access") == TokenType.ACCESS
    assert TokenType.from_text("Access") == TokenType.ACCESS
    assert TokenType.from_text("ACCESS") == TokenType.ACCESS
    assert TokenType.from_text("refresh") == TokenType.REFRESH

    with pytest.raises(InvalidTokenException):
        TokenType.from_text("acess")
