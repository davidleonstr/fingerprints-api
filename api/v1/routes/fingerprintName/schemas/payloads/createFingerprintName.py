from pydantic import BaseModel
from typing import Optional

class CreateFingerprintNameSchema(BaseModel):
    name: str
    description: Optional[str] = None