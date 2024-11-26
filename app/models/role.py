from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)  # Role ID
    name = Column(String, unique=True, index=True)  # Role name (e.g., "admin", "user")

    # Relationship back to User
    users = relationship("User", back_populates="role")  # Assuming User model has a relationship