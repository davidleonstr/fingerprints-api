from pydantic import BaseModel
from typing import Optional

class UpdateFingerprintSchema(BaseModel):
    template: Optional[str] = None
    fingerprint_type_id: Optional[int] = None
    fingerprint_name_id: Optional[int] = None
    is_active: Optional[bool] = None