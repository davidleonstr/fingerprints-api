from pydantic import BaseModel

class PermissionLevelData(BaseModel):
    permission_level: dict