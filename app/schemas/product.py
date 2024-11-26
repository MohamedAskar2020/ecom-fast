from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductImageBase(BaseModel):
    image_path: str

class ProductBase(BaseModel):
    name: str
    description: str
    original_price: float  # Original price of the product
    new_price: Optional[float] = None  # New price after discount (if applicable)
    images: List[ProductImageBase]  # List of images

class ProductCreate(ProductBase):
    pass  # You can add any additional fields needed for creating a product

class ProductUpdate(ProductBase):
    pass  # You can add any additional fields needed for updating a product

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Change from orm_mode to from_attributes
        arbitrary_types_allowed = True  # Allow arbitrary types if needed