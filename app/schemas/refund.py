from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RefundBase(BaseModel):
    order_id: int  # Foreign key to the Order model
    reason: str  # Reason for the refund
    amount: float  # Amount to be refunded
    status: str  # Status of the refund (e.g., "pending", "completed", "rejected")
    request_date: datetime  # Date when the refund was requested

class RefundCreate(RefundBase):
    pass  # You can add any additional fields needed for creating a refund

class RefundUpdate(RefundBase):
    status: Optional[str] = None  # Optional field for updating the status
    processed_date: Optional[datetime] = None  # Optional field for the processed date

class Refund(RefundBase):
    id: int  # Refund ID
    processed_date: Optional[datetime] = None  # Date when the refund was processed

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 