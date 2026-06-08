from api.config.database import DB

class AttendanceDayTime(DB.Model):
    __tablename__ = 'attendance_day_times'

    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name        = DB.Column(DB.String(50), unique=True, nullable=False)
    description = DB.Column(DB.Text)
    created_at  = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    attendances = DB.relationship('Attendance', back_populates='attendance_day_time')