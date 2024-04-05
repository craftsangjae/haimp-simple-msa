class HaimpException(Exception):
    message: str

    def __init__(self, message:str):
        self.message = message


class DatabaseException(HaimpException):
    """데이터 베이스에서 발생한 Exception """