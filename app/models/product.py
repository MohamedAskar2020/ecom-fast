from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)  # Product ID
    name = Column(String, nullable=False)  # Product name
    original_price = Column(Float, nullable=False)  # Original price of the product
    new_price = Column(Float, nullable=True)  # New price after discount (if applicable)
    stock = Column(Integer, nullable=False)  # Number of items in stock
    date_added = Column(DateTime, nullable=False)  # Date when the product was added
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User
    category_id = Column(Integer, ForeignKey('categories.id'))  # Foreign key to Category
    images = relationship("ProductImage", back_populates="product")  # Relationship to ProductImage

    # Relationships
    user = relationship("User", back_populates="products")  # Relationship to User
    category = relationship("Category", back_populates="products")  # Relationship to Category
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")  # Relationship to Review
    refunds = relationship("Refund", back_populates="product", cascade="all, delete-orphan")  # Relationship to Refund
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")  # Relationship to OrderItem

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    image_path = Column(String)

    product = relationship("Product", back_populates="images")  # Relationship back to Product