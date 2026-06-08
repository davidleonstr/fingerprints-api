from pydantic import BaseModel
from typing import Optional

class CreateAttendanceSchema(BaseModel):
    student_id: str
    attendance_date: str
    attendance_day_time_id: int
    attendance_method_id: int
    recorded_by_interactor_id: Optional[str] = None