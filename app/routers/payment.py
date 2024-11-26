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

# Create a new payment
@router.post("/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    new_payment = models.Payment(
        order_id=payment.order_id,
        payment_method_id=payment.payment_method_id,
        amount=payment.amount,
        status=payment.status,
        transaction_id=payment.transaction_id,
        payment_date=payment.payment_date,
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

# Get all payments
@router.get("/", response_model=list[schemas.Payment])
def get_all_payments(db: Session = Depends(get_db)):
    payments = db.query(models.Payment).all()
    return payments

# Get payment by ID
@router.get("/{payment_id}", response_model=schemas.Payment)
def get_payment_by_id(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# Update payment information
@router.put("/{payment_id}", response_model=schemas.Payment)
def update_payment(payment_id: int, payment_update: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    # Update payment fields
    if payment_update.status is not None:
        payment.status = payment_update.status
    if payment_update.transaction_id is not None:
        payment.transaction_id = payment_update.transaction_id

    db.commit()
    db.refresh(payment)
    return payment

# Delete a payment
@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db.delete(payment)
    db.commit()
    return 