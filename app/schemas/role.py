from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    name: str  # Name of the role

class RoleCreate(RoleBase):
    pass  # You can add any additional fields needed for creating a role

class RoleUpdate(RoleBase):
    pass  # You can add any additional fields needed for updating a role

class Role(RoleBase):
    id: int  # Role ID

    class Config:
        from_attributes = True  # Allows compatibility with ORM models 