from pydantic import BaseModel
 
class CreateInteractorSchema(BaseModel):
    username: str
    password: str
    entity_id: str
    role_id: int