import uuid
from api.config.database import DB

class FingerprintType(DB.Model):
    __tablename__ = 'fingerprint_types'

    id         = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name       = DB.Column(DB.String(20), unique=True, nullable=False)
    created_at = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    fingerprints = DB.relationship('Fingerprint', back_populates='fingerprint_type')