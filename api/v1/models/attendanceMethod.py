from api.config.database import DB

class AttendanceMethod(DB.Model):
    __tablename__ = 'attendance_methods'

    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name        = DB.Column(DB.String(30), unique=True, nullable=False)
    description = DB.Column(DB.Text)
    created_at  = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    attendances = DB.relationship('Attendance', back_populates='attendance_method')