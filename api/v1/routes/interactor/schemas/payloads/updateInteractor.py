from pydantic import BaseModel
from typing import Optional
 
class UpdateInteractorSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None