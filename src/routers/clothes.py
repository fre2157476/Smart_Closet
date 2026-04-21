from pathlib import Path
import shutil
from typing import Optional, List
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session
from random import choice
from fastapi import Query

from src.security import hash_password, verify_password
from src.ai.detect_clothing import ClothingDetector
from src.database.connection import get_db
from src.database.models import ClothingItem, DetectionResult
from src.schemas.clothing_schema import (
    ClothingItemResponse,
    OutfitRecommendationResponse
)

"""
Outfit Recommendation System (Color-Aware)

This section implements the outfit recommendation feature for the application.

Purpose:
- Generate a complete outfit from the user's saved clothing items
- Improve outfit quality using basic color-matching rules

Key Features:
1. Categorization:
   - Items are grouped into: top, bottom, dress, and footwear

2. Outfit Selection Logic:
   - If a dress is available, recommend: dress + footwear
   - Otherwise recommend: top + bottom + footwear

3. Color Matching Rules:
   - Neutral colors (black, white, gray, beige, brown) match with everything
   - Same colors are considered compatible
   - Blue bottoms (e.g., jeans) match most tops
   - If no match is found, fallback to random selection

4. Flexibility:
   - Supports filtering by season and occasion
   - Handles missing colors or categories gracefully

Helper Functions:
- colors_match(): Determines if two colors are compatible
- choose_matching_bottom(): Selects a bottom matching the top color
- choose_matching_footwear(): Selects footwear matching outfit color

Output:
- Returns a structured outfit recommendation using OutfitRecommendationResponse
"""


CATEGORY_LABELS = {
    "top": {"shirt", "long shirt", "sleeveless shirt", "hoodie", "jacket"},
    "bottom": {"long pants", "shorts", "long skirt", "short skirt"},
    "footwear": {"sport shoes", "flats", "high heels", "slipper"},
    "dress": {"dress"},
}

MIN_CONFIDENCE = 0.35
"""
Router:
- defines endpoints ( /clothes/upload )
"""

router = APIRouter(prefix="/clothes", tags=["Clothes"])

UPLOAD_DIR = Path("src/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

detector = ClothingDetector()

@router.post("/upload", response_model=ClothingItemResponse)
def upload_clothing(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    item_name: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    subcategory: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    season: Optional[str] = Form(None),
    occasion: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run detection
    all_detections = detector.detect(file_path, conf=0.05)

    best_detection = None
    clean_category = (
        category.strip().lower()
        if category and category.strip().lower() != "string"
        else None
    )

    # If user provided category, try matching it first
    if clean_category:
        matching_detections = [
            d for d in all_detections if d["category"] == clean_category
        ]

        if matching_detections:
            candidate = max(matching_detections, key=lambda d: d["confidence"])
            if candidate["confidence"] >= MIN_CONFIDENCE:
                best_detection = candidate

    # fallback to best YOLO detection overall
    if best_detection is None and all_detections:
        candidate = max(all_detections, key=lambda d: d["confidence"])
        if candidate["confidence"] >= MIN_CONFIDENCE:
            best_detection = candidate

    final_category = clean_category

    if best_detection and not final_category:
        final_category = best_detection["category"]

    if final_category is None:
        final_category = "unknown"

    final_subcategory = (
    subcategory.strip().lower()
    if subcategory and subcategory.strip().lower() != "string"
    else None
)
    final_color = color.strip().lower() \
        if color and color.strip().lower() != "string" \
        else None

    if best_detection:
        if not final_subcategory:
            final_subcategory = best_detection["label"]

    print("RAW color from form:", color)
    print("final_color before detect_color:", final_color)

    if not final_color:
        bbox = best_detection["bbox"] if best_detection else None
        final_color = detector.detect_color(file_path, bbox=bbox)

    # safety fallback
    if final_subcategory is None:
        final_subcategory = "unknown"

    if final_color is None:
        final_color = "unknown"


    new_item = ClothingItem(
        user_id=user_id,
        item_name=item_name,
        category=final_category,
        subcategory=final_subcategory,
        color=final_color,
        season=season,
        occasion=occasion,
        image_url=f"/uploads/{file.filename}"
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    """
    save YOLO detection in database"""
    if best_detection:
        detection_row = DetectionResult(
            clothing_item_id=new_item.id,
            detected_label=best_detection["label"],
            detected_color=final_color,
            confidence=best_detection["confidence"]
        )

        db.add(detection_row)
        db.commit()
    print("YOLO RESULT:", best_detection)

    return {
        "id": new_item.id,
        "user_id": new_item.user_id,
        "item_name": new_item.item_name,
        "category": new_item.category,
        "subcategory": new_item.subcategory,
        "color": new_item.color,
        "season": new_item.season,
        "occasion": new_item.occasion,
        "image_url": new_item.image_url,
        "detection": {
            "label": best_detection["label"],
            "confidence": best_detection["confidence"],
            "color": final_color
        } if best_detection else None
    }


@router.get("/",  response_model=List[ClothingItemResponse])
def get_clothes(
        category: Optional[str] = Query(None),
        user_id: Optional[int] = Query(None),
        db: Session = Depends(get_db)
):
    query = db.query(ClothingItem)

    if user_id is not None:
        query = query.filter(ClothingItem.user_id == user_id)

    if category and category.strip().lower() != "string":
        query = query.filter(ClothingItem.category == category.strip().lower())

    return query.all()


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ClothingItem).filter(ClothingItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Deleted"}


NEUTRAL_COLORS = {"black", "white", "gray", "grey", "beige", "brown"}
# Determines if two clothing colors are compatible
def colors_match(top_color: Optional[str], bottom_color: Optional[str]) -> bool:
    if not top_color or not bottom_color:
        return True

    top = top_color.lower()
    bottom = bottom_color.lower()

    if top in NEUTRAL_COLORS or bottom in NEUTRAL_COLORS:
        return True

    if top == bottom:
        return True

    if bottom == "blue":
        return True

    return False

# Select a bottom that matches the chosen top color
def choose_matching_bottom(chosen_top, bottoms):
    if not chosen_top or not bottoms:
        return None

    matching = [b for b in bottoms if colors_match(chosen_top.color, b.color)]
    return choice(matching) if matching else choice(bottoms)

# Select footwear that matches the outfit color
def choose_matching_footwear(item_color: Optional[str], footwear_items):
    if not footwear_items:
        return None

    if not item_color:
        return choice(footwear_items)

    matching = [
        shoe for shoe in footwear_items
        if colors_match(item_color, shoe.color)
    ]
    return choice(matching) if matching else choice(footwear_items)

@router.get("/recommend-outfit", response_model=OutfitRecommendationResponse)
def recommend_outfit(
    user_id: int = Query(...),
    season: Optional[str] = Query(None),
    occasion: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(ClothingItem).filter(ClothingItem.user_id == user_id)

    if season:
        query = query.filter(ClothingItem.season == season)

    if occasion:
        query = query.filter(ClothingItem.occasion == occasion)

    items = query.all()

    tops = [item for item in items if item.category == "top"]
    bottoms = [item for item in items if item.category == "bottom"]
    dresses = [item for item in items if item.category == "dress"]
    footwear = [item for item in items if item.category == "footwear"]

    # Dress outfit first
    if dresses and footwear:
        chosen_dress = choice(dresses)
        chosen_footwear = choose_matching_footwear(chosen_dress.color, footwear)

        return {
            "dress": chosen_dress,
            "footwear": chosen_footwear
        }

    # Top + bottom + footwear outfit
    if tops and bottoms and footwear:
        chosen_top = choice(tops)
        chosen_bottom = choose_matching_bottom(chosen_top, bottoms)
        chosen_footwear = choose_matching_footwear(chosen_bottom.color if chosen_bottom else None, footwear)

        return {
            "top": chosen_top,
            "bottom": chosen_bottom,
            "footwear": chosen_footwear
        }

    raise HTTPException(
        status_code=404,
        detail="Not enough clothing items to recommend a full outfit."
    )


@router.put("/{item_id}", response_model=ClothingItemResponse)
def update_item(
    item_id: int,
    item_name: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    subcategory: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    season: Optional[str] = Form(None),
    occasion: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    item = db.query(ClothingItem).filter(ClothingItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item_name is not None:
        item.item_name = item_name
    if category is not None:
        item.category = category
    if subcategory is not None:
        item.subcategory = subcategory
    if color is not None:
        item.color = color
    if season is not None:
        item.season = season
    if occasion is not None:
        item.occasion = occasion

    db.commit()
    db.refresh(item)
    return item