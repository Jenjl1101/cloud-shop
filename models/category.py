from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from .base import Base

class Category(Base):
    __tablename__ = 'categories'
    
    name = Column(String, primary_key=True)
    listing_count = Column(Integer, default=0)
    
    # Relationship
    listings = relationship("Listing", back_populates="category_relation")
    
    def __repr__(self):
        return f"<Category(name='{self.name}', count={self.listing_count})>"