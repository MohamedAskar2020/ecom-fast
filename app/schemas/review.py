from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    user_id: int  # Foreign key to the User model
    product_id: int  # Foreign key to the Product model
    rating: int  # Rating given by the user (e.g., 1 to 5)
    comment: Optional[str] = None  # Optional comment provided by the user

class ReviewCreate(ReviewBase):
    pass  # You can add any additional fields needed for creating a review

class ReviewUpdate(ReviewBase):
    rating: Optional[int] = None  # Optional field for updating the rating
    comment: Optional[str] = None  # Optional field for updating the comment

class Review(ReviewBase):
    id: int  # Review ID
    created_at: datetime  # Date when the review was created
    updated_at: Optional[datetime] = None  # Date when the review was last updated

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 