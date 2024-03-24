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
    class Config:
        schema_extra = {
            "example": {
                "FOV": 84,
                "AOI": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [77.395034, 28.49966],
                            [77.395077, 28.494889],
                            [77.401257, 28.495247],
                            [77.401085, 28.498302],
                            [77.395034, 28.49966]
                        ]
                    ]
                },
                "ImageHeight": 6000,
                "ImageWidth": 8000,
                "Overlap": 80,
                "Altitude": 100,
                "Speed": 15
            }
        }

