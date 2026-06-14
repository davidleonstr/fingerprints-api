from pydantic import BaseModel
from typing import Optional

class CreateFingerprintSchema(BaseModel):
    template: str
    assistable_id: str
    fingerprint_type_id: int
    fingerprint_name_id: int
    is_active: Optional[bool] = True