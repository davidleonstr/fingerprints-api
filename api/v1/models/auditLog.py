import uuid
from api.config.database import DB
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB

class AuditLog(DB.Model):
    __tablename__ = 'audit_log'

    id              = DB.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_name      = DB.Column(DB.String(100), nullable=False)
    record_id       = DB.Column(DB.Text, nullable=False)
    audit_action_id = DB.Column(DB.Integer, DB.ForeignKey('audit_actions.id'), nullable=False)
    interactor_id   = DB.Column(UUID(as_uuid=True), DB.ForeignKey('interactors.id', ondelete='SET NULL'), nullable=True)
    ip_address      = DB.Column(INET)
    old_data        = DB.Column(JSONB)
    new_data        = DB.Column(JSONB)
    created_at      = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    audit_action = DB.relationship('AuditAction', back_populates='audit_logs')
    interactor   = DB.relationship('Interactor',  back_populates='audit_logs')