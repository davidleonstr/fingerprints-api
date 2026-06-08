from api.config.database import DB

class PermissionLevel(DB.Model):
    __tablename__ = 'permission_levels'

    id          = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    number      = DB.Column(DB.Integer, unique=True, nullable=False)
    description = DB.Column(DB.Text)
    created_at  = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    roles = DB.relationship('Role', back_populates='permission_level')