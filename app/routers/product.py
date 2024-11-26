from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
import os
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.database import get_db

# Initialize the router
router = APIRouter()

# Directory to save uploaded images
UPLOAD_DIRECTORY = "uploads/products"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Dependency to get the database session


# Create a new product
@router.post("/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product.name,
        original_price=product.original_price,
        new_price=product.new_price,
        stock=product.stock,
        category_id=product.category_id,
        # Add other fields as necessary
        description=product.description,

    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # Save the uploaded images
    for image in product.images:
        file_location = os.path.join(UPLOAD_DIRECTORY, image.image_path)
        with open(file_location, "wb") as file_object:
            file_object.write(await image.read())
        
        # Create a ProductImage entry
        product_image = models.ProductImage(
            product_id=new_product.id,
            image_path=file_location
        )
        db.add(product_image)

    db.commit()  # Commit all changes
    return new_product

# Get all products
@router.get("/", response_model=list[schemas.Product])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# Get product by ID
@router.get("/{product_id}", response_model=schemas.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update product information
@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update product fields with division by zero checks
    if product_update.name:
        product.name = product_update.name
    if product_update.original_price is not None:
        if product_update.original_price <= 0:
            raise HTTPException(status_code=400, detail="Original price must be greater than zero")
        product.original_price = product_update.original_price
    if product_update.new_price is not None:
        if product_update.new_price < 0:
            raise HTTPException(status_code=400, detail="New price cannot be negative")
        product.new_price = product_update.new_price
    if product_update.stock is not None:
        product.stock = product_update.stock
    if product_update.category_id is not None:
        product.category_id = product_update.category_id

    db.commit()
    db.refresh(product)
    return product

# Delete a product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return 