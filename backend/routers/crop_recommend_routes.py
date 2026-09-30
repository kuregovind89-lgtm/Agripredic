import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models, schemas, auth
from ml.crop_recommend import recommend_crops
from ml.crop_data import SOIL_NPK_DEFAULTS

router = APIRouter(prefix="/api/crop", tags=["Crop Recommendation"])


@router.get("/soil-defaults")
def soil_defaults():
    """Typical N-P-K/pH values per soil type, for the 'I don't have a soil
    test report' fallback toggle on the frontend."""
    return SOIL_NPK_DEFAULTS


@router.post("/recommend", response_model=schemas.CropRecommendOut)
def recommend(
    payload: schemas.CropRecommendIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    results = recommend_crops(
        nitrogen=payload.nitrogen, phosphorus=payload.phosphorus, potassium=payload.potassium,
        temperature=payload.temperature, humidity=payload.humidity, ph=payload.soil_ph,
        rainfall=payload.rainfall, season=payload.season, soil_type=payload.soil_type,
    )

    record = models.CropRecommendation(
        user_id=current_user.id,
        soil_type=payload.soil_type, soil_ph=payload.soil_ph,
        nitrogen=payload.nitrogen, phosphorus=payload.phosphorus, potassium=payload.potassium,
        temperature=payload.temperature, humidity=payload.humidity, rainfall=payload.rainfall,
        season=payload.season, district=payload.district, state=payload.state,
        top_crop=results[0]["crop"], top_confidence=results[0]["confidence"],
        results_json=json.dumps(results),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id, "top_crop": record.top_crop, "top_confidence": record.top_confidence,
        "results": results, "created_at": record.created_at,
    }


@router.get("/history", response_model=List[schemas.CropRecommendOut])
def history(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    rows = (
        db.query(models.CropRecommendation)
        .filter(models.CropRecommendation.user_id == current_user.id)
        .order_by(models.CropRecommendation.created_at.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "id": r.id, "top_crop": r.top_crop, "top_confidence": r.top_confidence,
            "results": json.loads(r.results_json), "created_at": r.created_at,
        }
        for r in rows
    ]
