from pydantic import BaseModel

class MachineData(BaseModel):
    machine_id: str
    machine_name:str
    status:str
    time:str
    
    