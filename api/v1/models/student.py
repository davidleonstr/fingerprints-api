import uuid
from api.config.database import DB
from sqlalchemy.dialects.postgresql import UUID

class Student(DB.Model):
    __tablename__ = 'students'

    id           = DB.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id    = DB.Column(UUID(as_uuid=True), DB.ForeignKey('entities.id', ondelete='CASCADE'), unique=True)
    first_name   = DB.Column(DB.String(250), nullable=False)
    last_name    = DB.Column(DB.String(250), nullable=False)
    birthdate    = DB.Column(DB.Date, nullable=False)
    carnet       = DB.Column(DB.String(10), unique=True, nullable=False)
    email        = DB.Column(DB.String(250), unique=True, nullable=False)
    phone_number = DB.Column(DB.String(20), unique=True, nullable=False)
    is_active    = DB.Column(DB.Boolean, default=True)
    created_at   = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    entity       = DB.relationship('Entity',      back_populates='student')
    fingerprints = DB.relationship('Fingerprint', back_populates='student', cascade='all, delete-orphan')
    attendances  = DB.relationship('Attendance',  back_populates='student', cascade='all, delete-orphan')