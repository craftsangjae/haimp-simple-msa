from sqlalchemy import Column, Integer, String

from src.database import Base


class UserEntity(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_name = Column(String, unique=True)
    password = Column(String, nullable=False)

    user_group = Column(String, nullable=False)
    user_role = Column(String, nullable=False)