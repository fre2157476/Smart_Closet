from pydantic import BaseModel
from typing import Optional

class DetectionResponse(BaseModel):
    detected_label: str
    detected_color: Optional[str] = None
    confidence: Optional[float] = None


class ClothingItemResponse(BaseModel):
    id: int
    item_name: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    color: Optional[str] = None
    season: Optional[str] = None
    occasion: Optional[str] = None
    image_url: Optional[str] = None
    class Config:
        from_attributes = True

class OutfitItemMini(BaseModel):
    id: int
    item_name: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    color: Optional[str] = None
    season: Optional[str] = None
    occasion: Optional[str] = None
    image_url: str

    class Config:
        from_attributes = True

class OutfitRecommendationResponse(BaseModel):
    top: Optional[OutfitItemMini] = None
    bottom: Optional[OutfitItemMini] = None
    dress: Optional[OutfitItemMini] = None
    footwear: Optional[OutfitItemMini] = None
