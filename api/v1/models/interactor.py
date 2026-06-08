import uuid
from api.config.database import DB
from sqlalchemy.dialects.postgresql import UUID

class Interactor(DB.Model):
    __tablename__ = 'interactors'

    id            = DB.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username      = DB.Column(DB.String(250), unique=True, nullable=False)
    password_hash = DB.Column(DB.Text)
    entity_id     = DB.Column(UUID(as_uuid=True), DB.ForeignKey('entities.id', ondelete='CASCADE'), nullable=False)
    role_id       = DB.Column(DB.Integer, DB.ForeignKey('roles.id'), nullable=False)
    created_at    = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    entity = DB.relationship('Entity', back_populates='interactor')
    role   = DB.relationship('Role',   back_populates='interactors')

    recorded_attendances = DB.relationship(
        'Attendance',
        foreign_keys='Attendance.recorded_by_interactor_id',
        back_populates='recorded_by',
    )
    edited_attendances = DB.relationship(
        'Attendance',
        foreign_keys='Attendance.edited_by_interactor_id',
        back_populates='edited_by',
    )
    audit_logs = DB.relationship('AuditLog', back_populates='interactor')