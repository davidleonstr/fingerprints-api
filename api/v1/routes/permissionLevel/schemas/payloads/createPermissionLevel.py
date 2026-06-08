from pydantic import BaseModel
from typing import Optional

class CreatePermissionLevelSchema(BaseModel):
    number: int
    description: Optional[str] = None