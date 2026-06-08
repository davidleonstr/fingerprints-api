from pydantic import BaseModel

class AttendanceData(BaseModel):
    attendance: dict