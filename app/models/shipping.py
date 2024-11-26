from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Shipping(Base):
    __tablename__ = 'shippings'

    id = Column(Integer, primary_key=True, index=True)  # Shipping ID
    order_id = Column(Integer, ForeignKey('orders.id'))  # Foreign key to the Order model
    address_id = Column(Integer, ForeignKey('addresses.id'))  # Foreign key to the Address model
    shipping_date = Column(DateTime, nullable=True)  # Date when the shipping was initiated
    delivery_date = Column(DateTime, nullable=True)  # Expected or actual delivery date
    tracking_number = Column(String, nullable=True)  # Tracking number for the shipment
    carrier = Column(String, nullable=True)  # Shipping carrier (e.g., UPS, FedEx)
    status = Column(String)  # Status of the shipping (e.g., "pending", "shipped", "delivered")
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User model

    # Relationships
    user = relationship("User", back_populates="shippings")  # Assuming User model has a relationship
    order = relationship("Order", back_populates="shippings")  # Assuming Order model has a relationship
    address = relationship("Address", back_populates="shippings")  # Assuming Address model has a relationship

    # If you want to relate to User or Product, you can add those relationships as well

    # product_id = Column(Integer, ForeignKey('products.id'))  # Foreign key to Product model
    # product = relationship("Product", back_populates="shippings")  # Assuming Product model has a relationship