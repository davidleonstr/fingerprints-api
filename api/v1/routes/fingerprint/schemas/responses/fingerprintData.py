from pydantic import BaseModel

class FingerprintData(BaseModel):
    fingerprint: dict