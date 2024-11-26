from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

# Initialize the router
router = APIRouter()

# Dependency to get the database session


# Create a new address
@router.post("/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(database.get_db)):
    new_address = models.Address(
        user_id=address.user_id,
        street=address.street,
        city=address.city,
        state=address.state,
        zip_code=address.zip_code,
        country=address.country,
        is_default=address.is_default,
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

# Get all addresses
@router.get("/", response_model=list[schemas.Address])
def get_all_addresses(db: Session = Depends(database.get_db)):
    addresses = db.query(models.Address).all()
    return addresses

# Get address by ID
@router.get("/{address_id}", response_model=schemas.Address)
def get_address_by_id(address_id: int, db: Session = Depends(database.get_db)):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

# Update address information
@router.put("/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address_update: schemas.AddressUpdate, db: Session = Depends(database.get_db)):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    # Update address fields
    address.street = address_update.street
    address.city = address_update.city
    address.state = address_update.state
    address.zip_code = address_update.zip_code
    address.country = address_update.country
    address.is_default = address_update.is_default

    db.commit()
    db.refresh(address)
    return address

# Delete an address
@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(database.get_db)):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    db.delete(address)
    db.commit()
    return 