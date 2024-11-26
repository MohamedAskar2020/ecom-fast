from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)  # Review ID
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User
    product_id = Column(Integer, ForeignKey('products.id'))  # Foreign key to Product
    rating = Column(Integer)  # Rating given by the user (e.g., 1 to 5)
    comment = Column(String, nullable=True)  # Optional comment provided by the user

    # Relationships
    user = relationship("User", back_populates="reviews")  # Relationship to User
    product = relationship("Product", back_populates="reviews")  # Relationship to Product