from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    user_id: int  # Foreign key to the User model
    street: str  # Street address
    city: str  # City
    state: str  # State or region
    zip_code: str  # Postal or ZIP code
    country: str  # Country
    is_default: bool = False  # Indicates if this is the default address

class AddressCreate(AddressBase):
    pass  # You can add any additional fields needed for creating an address

class AddressUpdate(AddressBase):
    is_default: Optional[bool] = None  # Optional field for updating the default status

class Address(AddressBase):
    id: int  # Address ID

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 