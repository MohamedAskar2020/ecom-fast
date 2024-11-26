from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)  # Address ID
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to User
    street = Column(String, nullable=False)  # Street address
    city = Column(String, nullable=False)  # City
    state = Column(String, nullable=False)  # State
    zip_code = Column(String, nullable=False)  # ZIP or postal code
    country = Column(String, nullable=False)  # Country
    is_default = Column(Boolean, default=False)  # Indicates if this is the default address

    # Relationships
    user = relationship("User", back_populates="addresses")  # Relationship to User