from pydantic import BaseModel

class AttendanceDayTimeData(BaseModel):
    attendance_day_time: dict