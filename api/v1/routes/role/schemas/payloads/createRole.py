from pydantic import BaseModel
from typing import Optional

class CreateRoleSchema(BaseModel):
    name: str
    description: Optional[str] = None
    permission_level_id: int