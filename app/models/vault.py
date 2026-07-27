from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Vault(Base):
    __tablename__ = "vaults"

    id = Column(Integer, primary_key=True, index=True)

    website = Column(String(255), nullable=False)

    username = Column(String(255), nullable=False)

    password = Column(String(500), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")