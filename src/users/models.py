from sqlalchemy import Column, String

from src.database import Base


class UserEntity(Base):

    __tablename__ = "users"

    user_name = Column(String, primary_key=True)
    password = Column(String, nullable=False)

    user_group = Column(String, nullable=False)
    user_role = Column(String, nullable=False)
