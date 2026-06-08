import datetime
from uuid import UUID

def dumpModel(record) -> dict:
    if record is None:
        return {}
        
    result = {}
    for k, v in record.__dict__.items():
        if k.startswith('_'):
            continue
            
        if isinstance(v, (datetime.datetime, datetime.date)):
            result[k] = v.isoformat()
        elif isinstance(v, UUID):
            result[k] = str(v)
        elif isinstance(v, (str, int, float, bool, list, dict, type(None))):
            result[k] = v
            
    return result