from pydantic import BaseModel
from typing import Optional

class UpdatePermissionLevelSchema(BaseModel):
    number: Optional[int] = None
    description: Optional[str] = None