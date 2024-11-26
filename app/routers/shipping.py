from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

# Initialize the router
router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new shipping record
@router.post("/", response_model=schemas.Shipping)
def create_shipping(shipping: schemas.ShippingCreate, db: Session = Depends(get_db)):
    new_shipping = models.Shipping(
        order_id=shipping.order_id,
        address_id=shipping.address_id,
        shipping_date=shipping.shipping_date,
        delivery_date=shipping.delivery_date,
        tracking_number=shipping.tracking_number,
        carrier=shipping.carrier,
        status=shipping.status,
    )
    db.add(new_shipping)
    db.commit()
    db.refresh(new_shipping)
    return new_shipping

# Get all shipping records
@router.get("/", response_model=list[schemas.Shipping])
def get_all_shippings(db: Session = Depends(get_db)):
    shippings = db.query(models.Shipping).all()
    return shippings

# Get shipping record by ID
@router.get("/{shipping_id}", response_model=schemas.Shipping)
def get_shipping_by_id(shipping_id: int, db: Session = Depends(get_db)):
    shipping = db.query(models.Shipping).filter(models.Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="Shipping record not found")
    return shipping

# Update shipping information
@router.put("/{shipping_id}", response_model=schemas.Shipping)
def update_shipping(shipping_id: int, shipping_update: schemas.ShippingUpdate, db: Session = Depends(get_db)):
    shipping = db.query(models.Shipping).filter(models.Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="Shipping record not found")

    # Update shipping fields
    if shipping_update.tracking_number is not None:
        shipping.tracking_number = shipping_update.tracking_number
    if shipping_update.status is not None:
        shipping.status = shipping_update.status

    db.commit()
    db.refresh(shipping)
    return shipping

# Delete a shipping record
@router.delete("/{shipping_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipping(shipping_id: int, db: Session = Depends(get_db)):
    shipping = db.query(models.Shipping).filter(models.Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="Shipping record not found")
    
    db.delete(shipping)
    db.commit()
    return 