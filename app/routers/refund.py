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

# Create a new refund
@router.post("/", response_model=schemas.Refund)
def create_refund(refund: schemas.RefundCreate, db: Session = Depends(get_db)):
    new_refund = models.Refund(
        order_id=refund.order_id,
        reason=refund.reason,
        amount=refund.amount,
        status=refund.status,
        request_date=refund.request_date,
    )
    db.add(new_refund)
    db.commit()
    db.refresh(new_refund)
    return new_refund

# Get all refunds
@router.get("/", response_model=list[schemas.Refund])
def get_all_refunds(db: Session = Depends(get_db)):
    refunds = db.query(models.Refund).all()
    return refunds

# Get refund by ID
@router.get("/{refund_id}", response_model=schemas.Refund)
def get_refund_by_id(refund_id: int, db: Session = Depends(get_db)):
    refund = db.query(models.Refund).filter(models.Refund.id == refund_id).first()
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    return refund

# Update refund information
@router.put("/{refund_id}", response_model=schemas.Refund)
def update_refund(refund_id: int, refund_update: schemas.RefundUpdate, db: Session = Depends(get_db)):
    refund = db.query(models.Refund).filter(models.Refund.id == refund_id).first()
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")

    # Update refund fields
    if refund_update.status is not None:
        refund.status = refund_update.status
    if refund_update.processed_date is not None:
        refund.processed_date = refund_update.processed_date

    db.commit()
    db.refresh(refund)
    return refund

# Delete a refund
@router.delete("/{refund_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_refund(refund_id: int, db: Session = Depends(get_db)):
    refund = db.query(models.Refund).filter(models.Refund.id == refund_id).first()
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    
    db.delete(refund)
    db.commit()
    return 