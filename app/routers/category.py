from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.database import get_db
from app.config import UPLOAD_DIRECTORY
import os

# Initialize the router
router = APIRouter()

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Dependency to get the database session


# Create a new category
@router.post("/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save the uploaded file
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as file_object:
        file_object.write(await file.read())

    new_category = models.Category(
        name=category.name,
        description=category.description,
        image_path=file_location  # Store the file path
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get all categories
@router.get("/", response_model=list[schemas.Category])
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

# Get category by ID
@router.get("/{category_id}", response_model=schemas.Category)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Update category information
@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category_update: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Update category fields
    category.name = category_update.name
    category.description = category_update.description
    category.image = category_update.image
    category.product_ids = category_update.product_ids

    db.commit()
    db.refresh(category)
    return category

# Delete a category
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return 