from api.config.database import DB

class Role(DB.Model):
    __tablename__ = 'roles'

    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name                = DB.Column(DB.String(20), unique=True, nullable=False)
    description         = DB.Column(DB.Text)
    permission_level_id = DB.Column(DB.Integer, DB.ForeignKey('permission_levels.id'), nullable=False)
    created_at          = DB.Column(DB.DateTime(timezone=True), server_default=DB.func.now())

    permission_level = DB.relationship('PermissionLevel', back_populates='roles')
    interactors      = DB.relationship('Interactor', back_populates='role')