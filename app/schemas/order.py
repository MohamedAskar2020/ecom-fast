from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int  # Foreign key to the Product model
    quantity: int  # Quantity of the product ordered
    price: float  # Price of the product at the time of order

class OrderItemCreate(OrderItemBase):
    pass  # You can add any additional fields needed for creating an order item

class OrderItem(OrderItemBase):
    id: int  # Order item ID

    class Config:
        from_attributes = True  # Allows compatibility with ORM models

class OrderBase(BaseModel):
    user_id: int  # Foreign key to the User model
    order_date: datetime  # Date when the order was placed
    status: str  # Status of the order (e.g., "pending", "shipped", "delivered")
    total_amount: float  # Total amount for the order
    items: List[OrderItemBase]  # List of order items associated with the order

class OrderCreate(OrderBase):
    pass  # You can add any additional fields needed for creating an order

class OrderUpdate(OrderBase):
    status: Optional[str] = None  # Optional field for updating the status
    total_amount: Optional[float] = None  # Optional field for updating the total amount

class Order(OrderBase):
    id: int  # Order ID

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 