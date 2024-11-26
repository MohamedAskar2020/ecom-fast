from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Refund(Base):
    __tablename__ = 'refunds'

    id = Column(Integer, primary_key=True, index=True)  # Refund ID
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User
    order_id = Column(Integer, ForeignKey('orders.id'))  # Foreign key to Order
    product_id = Column(Integer, ForeignKey('products.id'))  # Foreign key to Product
    reason = Column(String)  # Reason for the refund
    amount = Column(Float)  # Amount to be refunded
    status = Column(String)  # Status of the refund (e.g., "pending", "completed", "rejected")

    # Relationships
    user = relationship("User", back_populates="refunds")  # Relationship to User
    order = relationship("Order", back_populates="refunds")  # Relationship to Order
    product = relationship("Product", back_populates="refunds")  # Relationship to Product