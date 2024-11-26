from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr  # Validates that the email is in the correct format
    full_name: Optional[str] = None  # Optional field for the user's full name
    is_active: bool = True  # Indicates if the user is active

class UserCreate(UserBase):
    password: str  # Password field for user creation

class UserUpdate(UserBase):
    password: Optional[str] = None  # Optional password field for updates
    disabled: Optional[bool] = None  # Optional field to indicate if the user is disabled

class User(UserBase):
    id: int  # User ID
    joined_date: datetime  # Date when the user joined
    role: str = "user"  # Default role is "user"
    
    # Relationships
    orders: List[Optional[int]] = []  # List of order IDs associated with the user
    products: List[Optional[int]] = []  # List of product IDs associated with the user
    addresses: List[Optional[int]] = []  # List of address IDs associated with the user
    shipping: List[Optional[int]] = []  # List of shipping IDs associated with the user
    reviews: List[Optional[int]] = []  # List of review IDs associated with the user
    cart: List[Optional[int]] = []  # List of cart IDs associated with the user
    refunds: List[Optional[int]] = []  # List of refund IDs associated with the user

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 