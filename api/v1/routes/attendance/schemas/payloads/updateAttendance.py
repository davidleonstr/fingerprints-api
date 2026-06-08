from pydantic import BaseModel
from typing import Optional

class UpdateAttendanceSchema(BaseModel):
    attendance_date: Optional[str] = None
    attendance_day_time_id: Optional[int] = None
    attendance_method_id: Optional[int] = None
    edited_by_interactor_id: Optional[str] = None