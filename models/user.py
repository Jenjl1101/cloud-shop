from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    username = Column(String, primary_key=True)
    listings = relationship("Listing", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"