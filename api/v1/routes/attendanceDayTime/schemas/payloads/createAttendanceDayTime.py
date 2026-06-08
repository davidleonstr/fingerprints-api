from pydantic import BaseModel
from typing import Optional

class CreateAttendanceDayTimeSchema(BaseModel):
    name: str
    description: Optional[str] = None