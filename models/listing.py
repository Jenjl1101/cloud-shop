from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from .base import Base

class Listing(Base):
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    username = Column(String, ForeignKey('users.username'), nullable=False)
    category = Column(String, ForeignKey('categories.name'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="listings")
    category_relation = relationship("Category", back_populates="listings")
    
    def __repr__(self):
        return f"<Listing(id={self.id}, title='{self.title}')>"