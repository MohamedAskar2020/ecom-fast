from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)  # Cart ID
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User
    total_amount = Column(Integer, default=0)  # Total amount for the cart

    # Relationships
    user = relationship("User", back_populates="cart", cascade="all, delete-orphan")  # Relationship to User
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")  # Relationship to CartItem

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)  # Cart item ID
    cart_id = Column(Integer, ForeignKey('carts.id'))  # Foreign key to Cart
    product_id = Column(Integer, ForeignKey('products.id'))  # Foreign key to Product
    quantity = Column(Integer, default=0)  # Quantity of the product in the cart
    price = Column(Integer, default=0)  # Price of the product at the time it was added to the cart

    # Relationships
    cart = relationship("Cart", back_populates="items")  # Relationship to Cart
    product = relationship("Product", back_populates="cart_items")  # Relationship to Product