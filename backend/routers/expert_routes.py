from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/expert", tags=["Agriculture Expert"])


@router.get("/farmers", response_model=List[schemas.UserOut])
def list_farmers(
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_role("admin", "expert")),
):
    return db.query(models.User).filter(models.User.role == "farmer").all()


@router.get("/predictions", response_model=List[schemas.PredictionOut])
def all_predictions(
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_role("admin", "expert")),
):
    return (
        db.query(models.Prediction)
        .order_by(models.Prediction.created_at.desc())
        .limit(100)
        .all()
    )


@router.get("/high-risk-farms")
def high_risk_farms(
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_role("admin", "expert")),
):
    rows = (
        db.query(models.RiskAssessment)
        .filter(models.RiskAssessment.overall_level == "High")
        .order_by(models.RiskAssessment.created_at.desc())
        .limit(50)
        .all()
    )
    result = []
    for r in rows:
        user = db.query(models.User).filter(models.User.id == r.user_id).first()
        result.append({
            "farmer_name": user.name if user else "Unknown",
            "location": r.location,
            "overall_level": r.overall_level,
            "crop_failure_risk": r.crop_failure_risk,
            "created_at": r.created_at,
        })
    return result
