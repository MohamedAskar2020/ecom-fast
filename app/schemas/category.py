from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str  # Name of the category
    description: Optional[str] = None  # Optional description of the category
    image_path: Optional[str] = None  # Optional image path for the category

    class Config:
        from_attributes = True  # Change from orm_mode to from_attributes
        arbitrary_types_allowed = True  # Allow arbitrary types if needed
        extra = "allow"  # Allow extra fields

class CategoryCreate(CategoryBase):
    pass  # You can add any additional fields needed for creating a category

class CategoryUpdate(CategoryBase):
    pass  # You can add any additional fields needed for updating a category

class Category(CategoryBase):
    id: int  # Category ID

    class Config:
        from_attributes = True  # Change from orm_mode to from_attributes
        arbitrary_types_allowed = True  # Allow arbitrary types if needed
        extra = "allow"  # Allow extra fields