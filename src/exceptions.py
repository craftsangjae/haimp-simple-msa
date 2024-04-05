class HaimpException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message


class DatabaseException(HaimpException):
    """데이터 베이스에서 발생한 Exception"""


class InvalidTokenException(HaimpException):
    """유효하지 않은 JWT 토큰인 경우"""


class InvalidUserException(HaimpException):
    """유저 정보가 잘못되었을 때"""
