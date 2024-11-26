from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShippingBase(BaseModel):
    order_id: int  # Foreign key to the Order model
    address_id: int  # Foreign key to the Address model
    shipping_date: Optional[datetime] = None  # Date when the shipping was initiated
    delivery_date: Optional[datetime] = None  # Expected or actual delivery date
    tracking_number: Optional[str] = None  # Tracking number for the shipment
    carrier: Optional[str] = None  # Shipping carrier (e.g., UPS, FedEx)
    status: str  # Status of the shipping (e.g., "pending", "shipped", "delivered")

class ShippingCreate(ShippingBase):
    pass  # You can add any additional fields needed for creating a shipping record

class ShippingUpdate(ShippingBase):
    tracking_number: Optional[str] = None  # Optional field for updating tracking number
    status: Optional[str] = None  # Optional field for updating status

class Shipping(ShippingBase):
    id: int  # Shipping ID
    # You can add relationships if needed, e.g., order details or address details

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 