from pathlib import Path
import shutil
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database.models import ClothingItem
from src.schemas.clothing_schema import ClothingItemResponse


router = APIRouter(prefix="/clothes", tags=["Clothes"])

UPLOAD_DIR = Path("src/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=ClothingItemResponse)
def upload_clothing(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    item_name: Optional[str] = Form(None),
    category: str = Form(...),
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

    new_item = ClothingItem(
        user_id=user_id,
        item_name=item_name,
        category=category,
        subcategory=subcategory,
        color=color,
        season=season,
        occasion=occasion,
        image_url=str(file_path)
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item