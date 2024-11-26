from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)  # Payment ID
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User
    order_id = Column(Integer, ForeignKey('orders.id'))  # Foreign key to Order
    amount = Column(Float, nullable=False)  # Amount paid
    status = Column(String, nullable=False)  # Status of the payment (e.g., "pending", "completed", "failed")
    transaction_id = Column(String, nullable=True)  # Transaction ID from the payment processor
    payment_date = Column(DateTime, nullable=False)  # Date when the payment was made

    # Relationships
    user = relationship("User", back_populates="payments")  # Relationship to User
    order = relationship("Order", back_populates="payments")  # Relationship to Order