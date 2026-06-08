from pydantic import BaseModel
from typing import Optional

class UpdateAttendanceMethodSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None