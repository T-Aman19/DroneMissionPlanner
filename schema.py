from pydantic import BaseModel
from typing import List
class MissionParameters(BaseModel):
    FOV:float
    AOI:dict
    ImageHeight: int
    ImageWidth: int
    Overlap:int
    Altitude:int
    Speed:int
