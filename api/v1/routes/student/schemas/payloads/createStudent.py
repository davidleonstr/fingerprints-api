from pydantic import BaseModel
from typing import Optional

class CreateStudentSchema(BaseModel):
    entity_id: str
    first_name: str
    last_name: str
    birthdate: str
    carnet: str
    email: str
    phone_number: str
    is_active: Optional[bool] = True