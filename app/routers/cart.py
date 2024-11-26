from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database

# Initialize the router
router = APIRouter()

# Dependency to get the database session


# Create a new cart
@router.post("/", response_model=schemas.Cart)
def create_cart(cart: schemas.CartCreate, db: Session = Depends(database.get_db)):
    new_cart = models.Cart(
        user_id=cart.user_id,
        total_amount=cart.total_amount,
        items=cart.items,
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

# Get all carts
@router.get("/", response_model=list[schemas.Cart])
def get_all_carts(db: Session = Depends(database.get_db)):
    carts = db.query(models.Cart).all()
    return carts

# Get cart by ID
@router.get("/{cart_id}", response_model=schemas.Cart)
def get_cart_by_id(cart_id: int, db: Session = Depends(database.get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

# Update cart information
@router.put("/{cart_id}", response_model=schemas.Cart)
def update_cart(cart_id: int, cart_update: schemas.CartUpdate, db: Session = Depends(database.get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Update cart fields
    cart.total_amount = cart_update.total_amount if cart_update.total_amount is not None else cart.total_amount
    cart.items = cart_update.items if cart_update.items is not None else cart.items

    db.commit()
    db.refresh(cart)
    return cart

# Delete a cart
@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(cart_id: int, db: Session = Depends(database.get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    db.delete(cart)
    db.commit()
    return

# Add item to cart
@router.post("/{cart_id}/items", response_model=schemas.Cart)
def add_item_to_cart(cart_id: int, item: schemas.CartItemCreate, db: Session = Depends(database.get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Add the item to the cart's items list
    cart.items.append(item)
    cart.total_amount += item.price * item.quantity  # Update total amount
    db.commit()
    db.refresh(cart)
    return cart

# Remove item from cart
@router.delete("/{cart_id}/items/{item_id}", response_model=schemas.Cart)
def remove_item_from_cart(cart_id: int, item_id: int, db: Session = Depends(database.get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Find the item in the cart
    item_to_remove = next((item for item in cart.items if item.id == item_id), None)
    if not item_to_remove:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    # Remove the item from the cart's items list
    cart.items.remove(item_to_remove)
    cart.total_amount -= item_to_remove.price * item_to_remove.quantity  # Update total amount
    db.commit()
    db.refresh(cart)
    return cart 