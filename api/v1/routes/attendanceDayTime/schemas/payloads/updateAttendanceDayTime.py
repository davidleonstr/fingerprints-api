from pydantic import BaseModel
from typing import Optional

class UpdateAttendanceDayTimeSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None