from pydantic import BaseModel
from typing import List, Optional

class CartItemBase(BaseModel):
    product_id: int  # Foreign key to the Product model
    quantity: int  # Quantity of the product in the cart
    price: float  # Price of the product at the time it was added to the cart

class CartItemCreate(CartItemBase):
    pass  # You can add any additional fields needed for creating a cart item

class CartItem(CartItemBase):
    id: int  # Cart item ID

    class Config:
        from_attributes = True  # Allows compatibility with ORM models

class CartBase(BaseModel):
    user_id: int  # Foreign key to the User model
    items: List[CartItemBase] = []  # List of cart items associated with the cart
    total_amount: float = 0.0  # Total amount for the items in the cart

class CartCreate(CartBase):
    pass  # You can add any additional fields needed for creating a cart

class CartUpdate(CartBase):
    total_amount: Optional[float] = None  # Optional field for updating the total amount

class Cart(CartBase):
    id: int  # Cart ID

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 