from pydantic import BaseModel

class AttendancesData(BaseModel):
    attendances: list