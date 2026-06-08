from pydantic import BaseModel
from typing import Optional

class UpdateFingerprintNameSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None