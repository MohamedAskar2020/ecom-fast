from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)  # Order item ID
    order_id = Column(Integer, ForeignKey('orders.id'))  # Foreign key to Order
    product_id = Column(Integer, ForeignKey('products.id'))  # Foreign key to Product
    quantity = Column(Integer)  # Quantity of the product ordered
    price = Column(Float)  # Price of the product at the time of order

    # Relationships
    order = relationship("Order", back_populates="order_items")  # Relationship to Order
    product = relationship("Product", back_populates="order_items")  # Relationship to Product

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)  # Order ID
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User
    order_date = Column(DateTime)  # Date when the order was placed
    status = Column(String)  # Status of the order (e.g., "pending", "completed")
    total_amount = Column(Float)  # Total amount for the order

    # Relationships
    user = relationship("User", back_populates="orders")  # Relationship to User
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")  # Relationship to OrderItem
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")  # Relationship to Payment