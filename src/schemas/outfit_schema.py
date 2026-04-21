from pydantic import BaseModel
from typing import List

class OutfitCreate(BaseModel):
    user_id: int
    name: str
    clothing_item_ids: List[int]

class OutfitResponse(BaseModel):
    id: int
    user_id: int
    name: str

    class Config:
        from_attributes = True