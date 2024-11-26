from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentMethodBase(BaseModel):
    name: str  # Name of the payment method (e.g., "Credit Card", "PayPal")
    description: Optional[str] = None  # Optional description of the payment method
    is_active: bool = True  # Indicates if the payment method is active

class PaymentMethodCreate(PaymentMethodBase):
    pass  # You can add any additional fields needed for creating a payment method

class PaymentMethodUpdate(PaymentMethodBase):
    pass  # You can add any additional fields needed for updating a payment method

class PaymentMethod(PaymentMethodBase):
    id: int  # Payment method ID

    class Config:
        from_attributes = True  # Allows compatibility with ORM models

class PaymentBase(BaseModel):
    order_id: int  # Foreign key to the Order model
    payment_method_id: int  # Foreign key to the PaymentMethod model
    amount: float  # Amount paid
    status: str  # Status of the payment (e.g., "pending", "completed", "failed")
    transaction_id: Optional[str] = None  # Transaction ID from the payment processor
    payment_date: datetime  # Date when the payment was made

class PaymentCreate(PaymentBase):
    pass  # You can add any additional fields needed for creating a payment

class PaymentUpdate(PaymentBase):
    status: Optional[str] = None  # Optional field for updating the status
    transaction_id: Optional[str] = None  # Optional field for updating the transaction ID

class Payment(PaymentBase):
    id: int  # Payment ID

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 