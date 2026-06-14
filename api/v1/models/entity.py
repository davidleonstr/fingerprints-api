import uuid
from api.config.database import DB
from sqlalchemy.dialects.postgresql import UUID

class Entity(DB.Model):
    __tablename__ = 'entities'

    id         = DB.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    assistable    = DB.relationship('Assistable',    back_populates='entity', uselist=False)
    interactor = DB.relationship('Interactor', back_populates='entity', uselist=False)