from api.config.database import DB

class AuditAction(DB.Model):
    __tablename__ = 'audit_actions'

    id         = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name       = DB.Column(DB.String(10), unique=True, nullable=False)
    created_at = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    audit_logs = DB.relationship('AuditLog', back_populates='audit_action')