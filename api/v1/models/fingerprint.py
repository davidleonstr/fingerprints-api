import uuid
from api.config.database import DB
from sqlalchemy.dialects.postgresql import UUID, BYTEA

class Fingerprint(DB.Model):
    __tablename__ = 'fingerprints'
    __table_args__ = (
        DB.UniqueConstraint('assistable_id', 'fingerprint_name_id', name='uq_assistable_finger_unique'),
    )

    id                  = DB.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template            = DB.Column(BYTEA, nullable=False)
    assistable_id          = DB.Column(UUID(as_uuid=True), DB.ForeignKey('assistable.id', ondelete='CASCADE'), nullable=False)
    fingerprint_type_id = DB.Column(DB.Integer, DB.ForeignKey('fingerprint_types.id'), nullable=False)
    fingerprint_name_id = DB.Column(DB.Integer, DB.ForeignKey('fingerprint_names.id'), nullable=False)
    is_active           = DB.Column(DB.Boolean, default=True)
    created_at          = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    assistable          = DB.relationship('Assistable',         back_populates='fingerprints')
    fingerprint_type = DB.relationship('FingerprintType', back_populates='fingerprints')
    fingerprint_name = DB.relationship('FingerprintName', back_populates='fingerprints')