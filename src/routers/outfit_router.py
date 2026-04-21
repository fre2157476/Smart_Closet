from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from src.database.connection import get_db
from src.database.models import Outfit, OutfitItem
from src.schemas.outfit_schema import OutfitCreate

router = APIRouter(prefix="/outfits", tags=["Outfits"])

@router.post("/")
def save_outfit(outfit: OutfitCreate, db: Session = Depends(get_db)):
    try:
        new_outfit = Outfit(
            user_id=outfit.user_id,
            outfit_name=outfit.name
        )
        db.add(new_outfit)
        db.commit()
        db.refresh(new_outfit)

        for clothing_item_id in outfit.clothing_item_ids:
            new_outfit_item = OutfitItem(
                outfit_id=new_outfit.id,
                clothing_item_id=clothing_item_id
            )
            db.add(new_outfit_item)

        db.commit()

        return {
            "message": "Outfit saved successfully",
            "outfit_id": new_outfit.id
        }

    except Exception as e:
        db.rollback()
        print("SAVE OUTFIT ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_outfits(
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Outfit)

    if user_id is not None:
        query = query.filter(Outfit.user_id == user_id)

    outfits = query.all()

    results = []

    for outfit in outfits:
        items = []

        for outfit_item in outfit.outfit_items:
            clothing_item = outfit_item.clothing_item

            if clothing_item:
                items.append({
                    "id": clothing_item.id,
                    "item_name": clothing_item.item_name,
                    "category": clothing_item.category,
                    "subcategory": clothing_item.subcategory,
                    "color": clothing_item.color,
                    "season": clothing_item.season,
                    "occasion": clothing_item.occasion,
                    "image_url": clothing_item.image_url,
                })

        results.append({
            "id": outfit.id,
            "outfit_name": outfit.outfit_name,
            "season": outfit.season,
            "occasion": outfit.occasion,
            "items": items
        })

    return results

@router.delete("/{outfit_id}")
def delete_outfit(outfit_id: int, db: Session = Depends(get_db)):
    outfit = db.query(Outfit).filter(Outfit.id == outfit_id).first()

    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")

    db.delete(outfit)
    db.commit()

    return {"message": "Outfit deleted successfully"}