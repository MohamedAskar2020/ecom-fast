from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)  # Category ID
    name = Column(String, unique=True, index=True)  # Category name
    description = Column(String, nullable=True)  # Optional description of the category
    image = Column(String, default="default.jpg")  # Field for the category image

    # Relationship to Product
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")  # Relationship to Product