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

# Create a new role
@router.post("/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    new_role = models.Role(
        name=role.name,
        # Add other fields as necessary
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# Get all roles
@router.get("/", response_model=list[schemas.Role])
def get_all_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return roles

# Get role by ID
@router.get("/{role_id}", response_model=schemas.Role)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Update role information
@router.put("/{role_id}", response_model=schemas.Role)
def update_role(role_id: int, role_update: schemas.RoleUpdate, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Update role fields
    role.name = role_update.name
    # Update other fields as necessary

    db.commit()
    db.refresh(role)
    return role

# Delete a role
@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.delete(role)
    db.commit()
    return 