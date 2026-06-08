from pydantic import BaseModel
from typing import Optional

class UpdateRoleSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_level_id: Optional[int] = None