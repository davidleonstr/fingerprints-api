from api.config.database import DB

class FingerprintName(DB.Model):
    __tablename__ = 'fingerprint_names'

    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name        = DB.Column(DB.String(25), unique=True, nullable=False)
    description = DB.Column(DB.Text)
    created_at  = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    fingerprints = DB.relationship('Fingerprint', back_populates='fingerprint_name')