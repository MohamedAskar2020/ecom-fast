from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import get_current_user  # Import the dependency to get the current user

# Initialize the router
router = APIRouter()

# Dependency to get the database session


# Create a new user
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled,
        password=user.password  # Ensure to hash the password in the model or service layer
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users (admin access)
@router.get("/", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

# Get user by ID
@router.get("/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get user by email
@router.get("/email/{email}", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get current user information
@router.get("/user", response_model=schemas.User)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user

# Update user information
@router.put("/user", response_model=schemas.User)
def update_user(user_update: schemas.UserUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if user_update.email:
        current_user.email = user_update.email
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.disabled is not None:
        current_user.disabled = user_update.disabled
    if user_update.password:
        current_user.password = user_update.password  # Ensure to hash the password here

    db.commit()
    db.refresh(current_user)
    return current_user

# Delete a user
@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    db.delete(current_user)
    db.commit()
    return 