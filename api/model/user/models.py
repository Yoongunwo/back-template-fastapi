from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship

from model.database import Base


class User(Base):
    __tablename__ = "user"

    uid = Column(BigInteger, primary_key=True, index=True)
    id = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
