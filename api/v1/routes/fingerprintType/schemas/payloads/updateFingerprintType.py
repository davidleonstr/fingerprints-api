from pydantic import BaseModel
from typing import Optional

class UpdateFingerprintTypeSchema(BaseModel):
    name: Optional[str] = None