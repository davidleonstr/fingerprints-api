import uuid
from api.config.database import DB
from sqlalchemy.dialects.postgresql import UUID

class Attendance(DB.Model):
    __tablename__ = 'attendance'
    __table_args__ = (
        DB.UniqueConstraint(
            'student_id', 'attendance_date', 'attendance_day_time_id',
            name='uq_student_id_date_unique',
        ),
    )

    id                        = DB.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id                = DB.Column(UUID(as_uuid=True), DB.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    attendance_date           = DB.Column(DB.Date, nullable=False)
    attendance_day_time_id    = DB.Column(DB.Integer, DB.ForeignKey('attendance_day_times.id'), nullable=False)
    attendance_method_id      = DB.Column(DB.Integer, DB.ForeignKey('attendance_methods.id'), nullable=False)
    recorded_by_interactor_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey('interactors.id', ondelete='SET NULL'), nullable=True)
    edited_by_interactor_id   = DB.Column(UUID(as_uuid=True), DB.ForeignKey('interactors.id', ondelete='SET NULL'), nullable=True)
    created_at                = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())
    edited_at                 = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    student             = DB.relationship('Student',           back_populates='attendances')
    attendance_day_time = DB.relationship('AttendanceDayTime', back_populates='attendances')
    attendance_method   = DB.relationship('AttendanceMethod',  back_populates='attendances')
    recorded_by         = DB.relationship(
        'Interactor',
        foreign_keys=[recorded_by_interactor_id],
        back_populates='recorded_attendances',
    )
    edited_by = DB.relationship(
        'Interactor',
        foreign_keys=[edited_by_interactor_id],
        back_populates='edited_attendances',
    )