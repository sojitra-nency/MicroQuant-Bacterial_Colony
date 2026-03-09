from pydantic import BaseModel
from typing import List


class ColonyCoordinate(BaseModel):
    x: int
    y: int


class AnalysisResponse(BaseModel):
    colony_count: int
    coordinates: List[ColonyCoordinate]
    result_image: str  # base64-encoded PNG


class ErrorResponse(BaseModel):
    detail: str
